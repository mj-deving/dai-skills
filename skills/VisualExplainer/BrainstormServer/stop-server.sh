#!/bin/bash
# Stop brainstorm server
# Usage: stop-server.sh <session-dir>
SESSION_DIR="$1"
[[ -z "$SESSION_DIR" ]] && echo '{"error":"Usage: stop-server.sh <session-dir>"}' && exit 1

PID_FILE="$SESSION_DIR/server.pid"
if [[ -f "$PID_FILE" ]]; then
  PID=$(cat "$PID_FILE")
  kill "$PID" 2>/dev/null
  sleep 2
  kill -9 "$PID" 2>/dev/null
  rm -f "$PID_FILE"
fi

# Clean up tmp sessions
[[ "$SESSION_DIR" == ${TMPDIR}/* ]] && rm -rf "$SESSION_DIR"
echo '{"status":"stopped"}'
