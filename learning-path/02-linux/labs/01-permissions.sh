#!/usr/bin/env bash
set -euo pipefail

base="${TMPDIR:-/tmp}/devops-mastery-linux-perm"
rm -rf "$base"
mkdir -p "$base/app/logs"
touch "$base/app/logs/app.log"

echo "== wrong: world-writable =="
chmod 777 "$base/app/logs" || true
ls -ld "$base/app/logs"

echo "== better: owner-only write on directory =="
chmod 750 "$base/app/logs"
chmod 640 "$base/app/logs/app.log"
ls -ld "$base/app/logs"
ls -l "$base/app/logs/app.log"

echo "== path execute bit demo =="
mkdir -p "$base/secret/dir"
echo hi >"$base/secret/dir/file"
chmod 700 "$base/secret"
if cat "$base/secret/dir/file" >/dev/null 2>&1; then
  echo "read file as $(id -un)"
else
  echo "cannot read (expected if you are not the owner in a shared lab)"
fi

if [[ "${KEEP:-0}" != "1" ]]; then
  rm -rf "$base"
  echo "cleaned $base"
else
  echo "kept $base"
fi
