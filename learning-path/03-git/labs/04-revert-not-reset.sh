#!/usr/bin/env bash
set -euo pipefail

root="${TMPDIR:-/tmp}/devops-mastery-git-04"
rm -rf "$root"
mkdir -p "$root"
cd "$root"

git init -b main
git config user.name "Lab User"
git config user.email "lab@example.com"
echo "ok" > svc.txt
git add svc.txt
git commit -m "Healthy config."
echo "bad" > svc.txt
git add svc.txt
git commit -m "Bad config that would ship."

echo "== revert the bad commit (shared-main safe) =="
git revert --no-edit HEAD
git log --oneline
echo "== last two diffs =="
git show --stat HEAD
echo "LAB_REPO=$root"
echo "Note: reset --hard would hide the mistake; revert keeps an audit trail."
