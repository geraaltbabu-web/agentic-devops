#!/usr/bin/env bash
set -euo pipefail

root="${TMPDIR:-/tmp}/devops-mastery-git-05"
rm -rf "$root"
mkdir -p "$root"
cd "$root"

git init -b main
git config user.name "Lab User"
git config user.email "lab@example.com"
echo "1.0.0" > VERSION
git add VERSION
git commit -m "Release candidate content."
git tag -a v1.0.0 -m "Release 1.0.0"
git show v1.0.0 --quiet --format=fuller
git rev-parse HEAD
echo "Image tag in CI would be git-$(git rev-parse --short HEAD)"
echo "LAB_REPO=$root"
