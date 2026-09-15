"""Runnable synthetic banking microservice. No real accounts or financial data."""

from __future__ import annotations

import hashlib
import json
import os
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SERVICE = os.getenv("SERVICE_NAME", "accounts")
PORT = int(os.getenv("PORT", "8080"))
DEPENDENCIES = {
    "accounts": [],
    "payments": ["accounts", "fraud", "ledger"],
    "ledger": [],
    "fraud": [],
    "notifications": [],
}


def assess_risk(amount: float, destination: str) -> dict:
    digest = int(hashlib.sha256(destination.encode()).hexdigest()[:4], 16)
    score = min(99, int(amount / 100) + digest % 25)
    return {"score": score, "decision": "review" if score >= 70 else "allow"}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args: object) -> None:
        event = {"ts": time.time(), "service": SERVICE, "message": fmt % args}
        print(json.dumps(event), flush=True)

    def json_response(self, status: int, payload: dict) -> None:
        body = json.dumps(payload).encode() + b"\n"
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("X-Correlation-ID", self.headers.get("X-Correlation-ID", str(uuid.uuid4())))
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        return json.loads(self.rfile.read(length) or b"{}")

    def do_GET(self) -> None:  # noqa: N802
        if self.path in ("/", "/health"):
            self.json_response(200, {
                "status": "ok", "service": SERVICE, "domain": "banking",
                "dependencies": DEPENDENCIES.get(SERVICE, []),
            })
        elif self.path == "/ready":
            self.json_response(200, {"ready": True, "service": SERVICE})
        elif self.path == "/accounts" and SERVICE == "accounts":
            self.json_response(200, {"accounts": [
                {"id": "acct-demo-001", "currency": "USD", "available": 2500.00},
                {"id": "acct-demo-002", "currency": "EUR", "available": 1800.00},
            ], "synthetic": True})
        elif self.path == "/transactions" and SERVICE == "ledger":
            self.json_response(200, {"transactions": [], "append_only": True, "synthetic": True})
        else:
            self.json_response(404, {"error": "route_not_found", "service": SERVICE})

    def do_POST(self) -> None:  # noqa: N802
        payload = self.read_json()
        if self.path == "/risk" and SERVICE == "fraud":
            self.json_response(200, assess_risk(float(payload.get("amount", 0)), payload.get("destination", "")))
        elif self.path == "/payments" and SERVICE == "payments":
            amount = float(payload.get("amount", 0))
            if amount <= 0:
                self.json_response(400, {"error": "amount_must_be_positive"})
                return
            self.json_response(202, {
                "payment_id": f"pay-{uuid.uuid4().hex[:12]}",
                "status": "accepted", "amount": amount,
                "currency": payload.get("currency", "USD"), "synthetic": True,
            })
        elif self.path == "/notifications" and SERVICE == "notifications":
            self.json_response(202, {"status": "queued", "channel": payload.get("channel", "email")})
        else:
            self.json_response(404, {"error": "route_not_found", "service": SERVICE})


if __name__ == "__main__":
    print(json.dumps({"event": "started", "service": SERVICE, "port": PORT}), flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
