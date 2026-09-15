#!/usr/bin/env bash
set -euo pipefail

echo "== addresses =="
ip -br addr || true
echo "== default route =="
ip route | head || true
echo "== listening TCP =="
ss -lnt | head -n 20 || true
echo "== DNS config =="
if command -v resolvectl >/dev/null 2>&1; then
  resolvectl status | head -n 40 || true
else
  cat /etc/resolv.conf || true
fi
echo "== curl example.com =="
if curl -sS -o /dev/null -w "http_code=%{http_code} time=%{time_total}\n" --max-time 8 https://example.com; then
  echo "outbound HTTPS works"
else
  echo "outbound HTTPS failed (ok on isolated labs). Read DNS/route/TLS from the error."
fi
