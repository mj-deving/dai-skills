#!/bin/bash
# Start brainstorm server for a session
# Usage: start-server.sh --project-dir /path/to/project [--port 3333] [--host 127.0.0.1]

# Create session directory
SESSION_DIR="${TMPDIR:-/tmp}/brainstorm-$$-$(date +%s)"
mkdir -p "$SESSION_DIR"

# Parse args
PORT="${BRAINSTORM_PORT:-3333}"
HOST="${BRAINSTORM_HOST:-127.0.0.1}"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --port) PORT="$2"; shift 2;;
    --host) HOST="$2"; shift 2;;
    --project-dir) PROJECT_DIR="$2"; shift 2;;
    --owner-pid) OWNER_PID="$2"; shift 2;;
    *) shift;;
  esac
done

# Write a waiting page
cat > "$SESSION_DIR/waiting.html" << 'EOF'
<div style="text-align:center;padding:60px;opacity:0.6">
  <h2>Waiting for content...</h2>
  <p>Claude is preparing design options for you.</p>
</div>
EOF

# Start server
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# BRAINSTORM_OWNER_PID is optional — if set, server auto-shuts down when parent dies.
# When called from Claude's Bash tool, PPID exits immediately, so we skip it by default.
# Pass --owner-pid explicitly if you want parent monitoring.
BRAINSTORM_PORT="$PORT" BRAINSTORM_HOST="$HOST" BRAINSTORM_DIR="$SESSION_DIR" \
  ${OWNER_PID:+BRAINSTORM_OWNER_PID=$OWNER_PID} \
  nohup node "$SCRIPT_DIR/server.cjs" > "$SESSION_DIR/server.log" 2>&1 &

echo $! > "$SESSION_DIR/server.pid"

# Wait for startup
for i in $(seq 1 50); do
  if grep -q "server-started" "$SESSION_DIR/server.log" 2>/dev/null; then
    echo "{\"url\": \"http://${HOST}:${PORT}\", \"session_dir\": \"${SESSION_DIR}\"}"
    exit 0
  fi
  sleep 0.1
done

echo "{\"error\": \"Server failed to start within 5 seconds\"}"
exit 1
