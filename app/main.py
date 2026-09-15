"""Synthetic clinic API for the health-domain DevOps demo. No real patient data."""

from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

SERVICE = "clinic-api"

# Fake clinic slots only — not PHI, not a real hospital system.
APPOINTMENTS = [
    {"id": "apt-1001", "clinic": "riverside-wellness", "specialty": "general-practice", "slot": "2026-09-16T09:00:00Z", "status": "open"},
    {"id": "apt-1002", "clinic": "riverside-wellness", "specialty": "cardiology", "slot": "2026-09-16T11:30:00Z", "status": "open"},
    {"id": "apt-1003", "clinic": "lakeside-care", "specialty": "pediatrics", "slot": "2026-09-17T14:00:00Z", "status": "open"},
]


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args) -> None:  # noqa: A003
        return

    def _json(self, code: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8") + b"\n"
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if self.path in ("/", "/health"):
            self._json(200, {"status": "ok", "service": SERVICE, "domain": "health"})
            return
        if self.path == "/appointments":
            self._json(200, {"service": SERVICE, "appointments": APPOINTMENTS})
            return
        self.send_response(404)
        self.end_headers()


def main() -> None:
    port = int(os.environ.get("PORT", "8080"))
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"{SERVICE} listening on :{port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
