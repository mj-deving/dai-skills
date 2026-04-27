/**
 * BrainstormServer — Zero-dependency Node.js HTTP + WebSocket server
 *
 * Architecture: File-based communication between Claude and the browser.
 * Claude writes HTML fragments to a watched directory, this server auto-serves
 * them, the user clicks choices in the browser, and choices are appended to an
 * events file (.events) that Claude reads on the next turn.
 *
 * Origin: Adapted from obra/superpowers brainstorming server (MIT)
 *
 * Environment variables:
 *   BRAINSTORM_PORT      — HTTP port (default 3333)
 *   BRAINSTORM_HOST      — Bind address (default 127.0.0.1)
 *   BRAINSTORM_DIR       — Session directory to watch for HTML files
 *   BRAINSTORM_OWNER_PID — Parent PID; server shuts down if parent dies
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const ws = require('./websocket.cjs');

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------

const PORT = parseInt(process.env.BRAINSTORM_PORT || '3333', 10);
const HOST = process.env.BRAINSTORM_HOST || '127.0.0.1';
const SESSION_DIR = process.env.BRAINSTORM_DIR;
const OWNER_PID = process.env.BRAINSTORM_OWNER_PID
  ? parseInt(process.env.BRAINSTORM_OWNER_PID, 10)
  : null;

if (!SESSION_DIR) {
  console.error('BRAINSTORM_DIR is required');
  process.exit(1);
}

const SCRIPT_DIR = __dirname;
const EVENTS_FILE = path.join(SESSION_DIR, '.events');
const STATE_FILE = path.join(SESSION_DIR, 'state.json');
const INACTIVITY_TIMEOUT_MS = 30 * 60 * 1000; // 30 minutes
const WATCH_DEBOUNCE_MS = 200;

// ---------------------------------------------------------------------------
// State
// ---------------------------------------------------------------------------

let lastActivity = Date.now();
const wsClients = new Set();
let frameTemplate = null;

function touchActivity() { lastActivity = Date.now(); }

// ---------------------------------------------------------------------------
// Utility: MIME types
// ---------------------------------------------------------------------------

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.htm': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
  '.webp': 'image/webp',
};

function getMime(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  return MIME_TYPES[ext] || 'application/octet-stream';
}

// ---------------------------------------------------------------------------
// HTML utilities: newest file, fragment detection, template wrapping
// ---------------------------------------------------------------------------

function getNewestHtml() {
  try {
    const files = fs.readdirSync(SESSION_DIR)
      .filter(f => f.endsWith('.html'))
      .map(f => ({ name: f, mtime: fs.statSync(path.join(SESSION_DIR, f)).mtimeMs }))
      .sort((a, b) => b.mtime - a.mtime);
    return files.length > 0 ? files[0].name : null;
  } catch { return null; }
}

function getFrameTemplate() {
  if (!frameTemplate) {
    const templatePath = path.join(SCRIPT_DIR, 'frame-template.html');
    try {
      frameTemplate = fs.readFileSync(templatePath, 'utf-8');
    } catch {
      frameTemplate = '<!DOCTYPE html><html><head><meta charset="utf-8"><title>Brainstorm</title></head><body>{{CONTENT}}<script src="/helper.js"></script></body></html>';
    }
  }
  return frameTemplate;
}

function isFragment(html) {
  const lower = html.slice(0, 500).toLowerCase();
  return !lower.includes('<html') && !lower.includes('<!doctype');
}

function wrapFragment(html) {
  return getFrameTemplate().replace('{{CONTENT}}', html);
}

// ---------------------------------------------------------------------------
// State file management
// ---------------------------------------------------------------------------

function updateState(patch) {
  let state = {};
  try { state = JSON.parse(fs.readFileSync(STATE_FILE, 'utf-8')); } catch {}
  Object.assign(state, patch, { updatedAt: new Date().toISOString() });
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2), 'utf-8');
}

// ---------------------------------------------------------------------------
// WebSocket message handler (choice events)
// ---------------------------------------------------------------------------

function handleWsMessage(raw, _socket) {
  try {
    const msg = JSON.parse(raw);
    if (msg.type === 'choice') {
      const event = {
        type: 'choice',
        choice: msg.choice,
        timestamp: msg.timestamp || new Date().toISOString(),
      };
      fs.appendFileSync(EVENTS_FILE, JSON.stringify(event) + '\n', 'utf-8');
      updateState({ lastChoice: event });
    }
  } catch {
    // Ignore malformed messages
  }
}

// ---------------------------------------------------------------------------
// HTTP server
// ---------------------------------------------------------------------------

const server = http.createServer((req, res) => {
  touchActivity();
  const parsedUrl = new URL(req.url, `http://${HOST}:${PORT}`);
  const pathname = parsedUrl.pathname;

  // GET / — serve newest HTML file
  if (pathname === '/' || pathname === '/index.html') {
    const newest = getNewestHtml();
    if (!newest) {
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(wrapFragment('<div style="text-align:center;padding:60px;opacity:0.6"><h2>Waiting for content...</h2><p>Claude is preparing design options for you.</p></div>'));
      return;
    }
    try {
      let html = fs.readFileSync(path.join(SESSION_DIR, newest), 'utf-8');
      if (isFragment(html)) {
        html = wrapFragment(html);
      } else if (!html.includes('helper.js')) {
        html = html.replace('</body>', '<script src="/helper.js"></script></body>');
      }
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(html);
    } catch (err) {
      res.writeHead(500, { 'Content-Type': 'text/plain' });
      res.end('Error reading file: ' + err.message);
    }
    return;
  }

  // GET /helper.js — serve WebSocket client library
  if (pathname === '/helper.js') {
    try {
      const content = fs.readFileSync(path.join(SCRIPT_DIR, 'helper.js'), 'utf-8');
      res.writeHead(200, { 'Content-Type': 'application/javascript; charset=utf-8' });
      res.end(content);
    } catch (err) {
      res.writeHead(500, { 'Content-Type': 'text/plain' });
      res.end('Error reading helper.js: ' + err.message);
    }
    return;
  }

  // GET /files/* — serve static assets from session directory
  if (pathname.startsWith('/files/')) {
    const relativePath = pathname.slice('/files/'.length);
    const filePath = path.join(SESSION_DIR, relativePath);
    // Prevent directory traversal
    if (!filePath.startsWith(SESSION_DIR)) {
      res.writeHead(403, { 'Content-Type': 'text/plain' });
      res.end('Forbidden');
      return;
    }
    try {
      const content = fs.readFileSync(filePath);
      res.writeHead(200, { 'Content-Type': getMime(filePath) });
      res.end(content);
    } catch {
      res.writeHead(404, { 'Content-Type': 'text/plain' });
      res.end('Not found');
    }
    return;
  }

  // 404
  res.writeHead(404, { 'Content-Type': 'text/plain' });
  res.end('Not found');
});

// ---------------------------------------------------------------------------
// WebSocket upgrade handling
// ---------------------------------------------------------------------------

server.on('upgrade', (req, socket, _head) => {
  if (!ws.upgradeSocket(req, socket)) return;
  ws.handleConnection(socket, {
    clients: wsClients,
    onMessage: handleWsMessage,
    onActivity: touchActivity,
  });
});

// ---------------------------------------------------------------------------
// File watching: debounced fs.watch on session directory
// ---------------------------------------------------------------------------

let watchTimeout = null;

function startWatching() {
  try {
    fs.watch(SESSION_DIR, { persistent: false }, (_eventType, filename) => {
      if (!filename || !filename.endsWith('.html')) return;
      if (watchTimeout) clearTimeout(watchTimeout);
      watchTimeout = setTimeout(() => {
        if (filename === 'frame-template.html') frameTemplate = null;
        ws.broadcast(wsClients, { type: 'reload' });
      }, WATCH_DEBOUNCE_MS);
    });
  } catch (err) {
    console.error('File watching error:', err.message);
  }
}

// ---------------------------------------------------------------------------
// Lifecycle: inactivity shutdown, owner monitoring
// ---------------------------------------------------------------------------

function checkInactivity() {
  if (Date.now() - lastActivity > INACTIVITY_TIMEOUT_MS) {
    console.log('Shutting down due to inactivity');
    shutdown();
  }
}

function checkOwnerProcess() {
  if (!OWNER_PID) return;
  try { process.kill(OWNER_PID, 0); } catch {
    console.log('Owner process gone, shutting down');
    shutdown();
  }
}

function shutdown() {
  updateState({ status: 'stopped', stoppedAt: new Date().toISOString() });
  for (const client of wsClients) {
    try {
      client.write(ws.encodeFrame(ws.OPCODES.CLOSE, Buffer.alloc(0)));
      client.end();
    } catch {}
  }
  wsClients.clear();
  server.close(() => process.exit(0));
  setTimeout(() => process.exit(0), 3000);
}

// ---------------------------------------------------------------------------
// Start
// ---------------------------------------------------------------------------

server.listen(PORT, HOST, () => {
  const startInfo = {
    status: 'running',
    url: `http://${HOST}:${PORT}`,
    sessionDir: SESSION_DIR,
    startedAt: new Date().toISOString(),
    pid: process.pid,
  };
  updateState(startInfo);
  console.log(`server-started ${JSON.stringify(startInfo)}`);
  startWatching();
  setInterval(checkInactivity, 60 * 1000);
  if (OWNER_PID) setInterval(checkOwnerProcess, 10 * 1000);
});

process.on('SIGTERM', shutdown);
process.on('SIGINT', shutdown);
