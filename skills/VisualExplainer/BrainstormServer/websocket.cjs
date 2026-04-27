/**
 * WebSocket protocol implementation (RFC 6455)
 *
 * Zero-dependency. Handles handshake, frame encoding/decoding,
 * and client connection management.
 */

const crypto = require('crypto');

const OPCODES = {
  TEXT: 0x01,
  CLOSE: 0x08,
  PING: 0x09,
  PONG: 0x0A,
};

/**
 * Compute Sec-WebSocket-Accept key for handshake
 */
function computeAcceptKey(clientKey) {
  const GUID = '258EAFA5-E914-47DA-95CA-5AB5DC11D65B';
  return crypto.createHash('sha1').update(clientKey + GUID).digest('base64');
}

/**
 * Encode a WebSocket frame (server-to-client, unmasked)
 */
function encodeFrame(opcode, payload) {
  const data = Buffer.isBuffer(payload) ? payload : Buffer.from(payload, 'utf-8');
  const len = data.length;
  let header;

  if (len < 126) {
    header = Buffer.alloc(2);
    header[0] = 0x80 | opcode;
    header[1] = len;
  } else if (len < 65536) {
    header = Buffer.alloc(4);
    header[0] = 0x80 | opcode;
    header[1] = 126;
    header.writeUInt16BE(len, 2);
  } else {
    header = Buffer.alloc(10);
    header[0] = 0x80 | opcode;
    header[1] = 127;
    header.writeBigUInt64BE(BigInt(len), 2);
  }

  return Buffer.concat([header, data]);
}

/**
 * Decode a WebSocket frame from a buffer (client-to-server, masked)
 * Returns { opcode, payload, totalLength } or null if incomplete
 */
function decodeFrame(buffer) {
  if (buffer.length < 2) return null;

  const firstByte = buffer[0];
  const secondByte = buffer[1];
  const opcode = firstByte & 0x0F;
  const masked = (secondByte & 0x80) !== 0;
  let payloadLength = secondByte & 0x7F;
  let offset = 2;

  if (payloadLength === 126) {
    if (buffer.length < 4) return null;
    payloadLength = buffer.readUInt16BE(2);
    offset = 4;
  } else if (payloadLength === 127) {
    if (buffer.length < 10) return null;
    payloadLength = Number(buffer.readBigUInt64BE(2));
    offset = 10;
  }

  let maskKey = null;
  if (masked) {
    if (buffer.length < offset + 4) return null;
    maskKey = buffer.slice(offset, offset + 4);
    offset += 4;
  }

  if (buffer.length < offset + payloadLength) return null;

  let payload = buffer.slice(offset, offset + payloadLength);
  if (masked && maskKey) {
    for (let i = 0; i < payload.length; i++) {
      payload[i] ^= maskKey[i % 4];
    }
  }

  return { opcode, payload, totalLength: offset + payloadLength };
}

/**
 * Perform WebSocket upgrade handshake on a socket
 */
function upgradeSocket(req, socket) {
  const key = req.headers['sec-websocket-key'];
  if (!key) {
    socket.destroy();
    return false;
  }

  const acceptKey = computeAcceptKey(key);
  const headers = [
    'HTTP/1.1 101 Switching Protocols',
    'Upgrade: websocket',
    'Connection: Upgrade',
    `Sec-WebSocket-Accept: ${acceptKey}`,
    '',
    '',
  ].join('\r\n');

  socket.write(headers);
  return true;
}

/**
 * Create a WebSocket connection handler
 *
 * @param {Object} opts
 * @param {Set} opts.clients - Set of connected sockets
 * @param {Function} opts.onMessage - Called with (text, socket) for TEXT frames
 * @param {Function} opts.onActivity - Called on any activity (for inactivity tracking)
 */
function handleConnection(socket, opts) {
  const { clients, onMessage, onActivity } = opts;
  clients.add(socket);
  if (onActivity) onActivity();

  let buffer = Buffer.alloc(0);

  socket.on('data', (data) => {
    if (onActivity) onActivity();
    buffer = Buffer.concat([buffer, data]);

    while (buffer.length > 0) {
      const frame = decodeFrame(buffer);
      if (!frame) break;
      buffer = buffer.slice(frame.totalLength);

      switch (frame.opcode) {
        case OPCODES.TEXT:
          if (onMessage) onMessage(frame.payload.toString('utf-8'), socket);
          break;
        case OPCODES.PING:
          try { socket.write(encodeFrame(OPCODES.PONG, frame.payload)); } catch {}
          break;
        case OPCODES.CLOSE:
          try { socket.write(encodeFrame(OPCODES.CLOSE, Buffer.alloc(0))); } catch {}
          clients.delete(socket);
          socket.end();
          break;
        case OPCODES.PONG:
          break;
      }
    }
  });

  socket.on('close', () => clients.delete(socket));
  socket.on('error', () => clients.delete(socket));
}

/**
 * Broadcast a JSON message to all connected clients
 */
function broadcast(clients, data) {
  const frame = encodeFrame(OPCODES.TEXT, JSON.stringify(data));
  for (const client of clients) {
    try {
      client.write(frame);
    } catch {
      clients.delete(client);
    }
  }
}

module.exports = {
  OPCODES,
  computeAcceptKey,
  encodeFrame,
  decodeFrame,
  upgradeSocket,
  handleConnection,
  broadcast,
};
