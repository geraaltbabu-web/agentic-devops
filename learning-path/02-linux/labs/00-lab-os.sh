#!/usr/bin/env bash
set -euo pipefail
export SYSTEMD_PAGER=cat

echo "== kernel =="
uname -a
echo "== user =="
id
echo "== cwd =="
pwd
echo "== disk =="
df -h /
echo "== systemd =="
if command -v systemctl >/dev/null 2>&1 && systemctl is-system-running >/dev/null 2>&1; then
  systemctl is-system-running
else
  echo "systemd not fully available (common on some WSL setups). Use a VM for unit labs."
fi
echo "== shell =="
echo "$BASH_VERSION"
