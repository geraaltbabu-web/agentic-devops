#!/usr/bin/env bash
set -euo pipefail

root="${TMPDIR:-/tmp}/devops-mastery-git-02"
rm -rf "$root"
mkdir -p "$root"
cd "$root"

git init -b main
git config user.name "Lab User"
git config user.email "lab@example.com"
echo "base" > app.txt
git add app.txt
git commit -m "Base file."

git switch -c feat/note
echo "feature" >> app.txt
git add app.txt
git commit -m "Add feature line."

git switch main
echo "hot" >> app.txt
git add app.txt
git commit -m "Add hotfix line on main."

git merge feat/note -m "Merge feat/note." || {
  echo "== conflict expected if both edited same lines; resolving for the lab =="
  printf "base\nhot\nfeature\n" > app.txt
  git add app.txt
  git commit -m "Merge feat/note (resolved)."
}

git log --oneline --graph --decorate --all
echo "LAB_REPO=$root"
