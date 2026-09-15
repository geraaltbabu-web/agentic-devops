#!/usr/bin/env bash
set -euo pipefail

port="${PORT:-18080}"
if py -3 -c "import sys" >/dev/null 2>&1; then
  py=(py -3)
elif python -c "import sys" >/dev/null 2>&1; then
  py=(python)
elif python3 -c "import sys" >/dev/null 2>&1; then
  py=(python3)
else
  echo "Python not installed. Skip this lab or install Python 3."
  exit 0
fi

PORT="$port" "${py[@]}" - <<'PY' &
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

class H(BaseHTTPRequestHandler):
    def log_message(self, *args):
        return

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok\n")

HTTPServer(("127.0.0.1", int(os.environ["PORT"])), H).serve_forever()
PY
pid=$!
trap 'kill $pid 2>/dev/null || true' EXIT
sleep 0.8

echo "== process =="
ps -p "$pid" || true
echo "== listeners =="
ss -lnt 2>/dev/null | grep "$port" || netstat -an 2>/dev/null | grep "$port" || true
echo "== curl =="
curl -sS --max-time 2 "http://127.0.0.1:${port}/"
echo
echo "stopping pid $pid"
