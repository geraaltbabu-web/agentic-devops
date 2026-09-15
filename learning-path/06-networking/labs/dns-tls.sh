#!/usr/bin/env bash
set -euo pipefail
echo "== DNS =="
getent hosts example.com || ping -n 1 example.com || true
echo "== curl verbose headers (first 40 lines) =="
curl -sSI --max-time 10 https://example.com | head -n 40
echo "== openssl cert dates (if openssl exists) =="
if command -v openssl >/dev/null; then
  echo | openssl s_client -servername example.com -connect example.com:443 2>/dev/null | openssl x509 -noout -dates -subject || true
fi
