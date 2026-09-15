#!/usr/bin/env bash
set -euo pipefail

echo "== space vs inodes on / =="
df -h /
df -i /

base="${TMPDIR:-/tmp}/devops-mastery-linux-inodes"
rm -rf "$base"
mkdir -p "$base"

echo "== creating 200 tiny files (safe cap) =="
for i in $(seq 1 200); do
  : >"$base/f-$i"
done
echo "files=$(find "$base" | wc -l)"
df -i "$base" 2>/dev/null || df -i /

rm -rf "$base"
echo "cleaned $base"
