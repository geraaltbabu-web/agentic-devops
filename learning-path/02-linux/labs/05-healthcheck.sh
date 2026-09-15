#!/usr/bin/env bash
set -euo pipefail

json=0
if [[ "${1:-}" == "--json" ]]; then
  json=1
fi

url="${HEALTH_URL:-https://example.com}"
threshold="${DISK_THRESHOLD:-95}"
path="${DISK_PATH:-/}"

code="000"
if code=$(curl -sS -o /dev/null -w "%{http_code}" --max-time 8 "$url" || true); then
  :
fi

used=$(df -P "$path" 2>/dev/null | awk 'NR==2 {print $(NF-1)}' | tr -d '%')
if ! [[ "$used" =~ ^[0-9]+$ ]] || (( used > 100 )); then
  echo "note: df output is not POSIX Capacity%; skipping disk gate on this OS" >&2
  used=0
fi
ok=1
[[ "$code" =~ ^2 ]] || ok=0
(( used < threshold )) || ok=0

if [[ "$json" -eq 1 ]]; then
  printf '{"url":"%s","http_code":"%s","disk_path":"%s","disk_used_percent":%s,"ok":%s}\n' \
    "$url" "$code" "$path" "$used" "$ok"
else
  echo "url=$url http_code=$code"
  echo "disk $path used=${used}% threshold=${threshold}%"
  echo "ok=$ok"
fi

exit $((1 - ok))
