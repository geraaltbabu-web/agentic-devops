#!/usr/bin/env bash
set -euo pipefail

root="${TMPDIR:-/tmp}/devops-mastery-git-01"
rm -rf "$root"
mkdir -p "$root"
cd "$root"

git init -b main
git config user.name "Lab User"
git config user.email "lab@example.com"
echo "# demo" > README.md
git add README.md
git commit -m "Add README."
echo "ignored" > .env
echo ".env" > .gitignore
git add .gitignore
git commit -m "Ignore local env files."
git check-ignore -v .env
git log --oneline --decorate
echo "LAB_REPO=$root"
