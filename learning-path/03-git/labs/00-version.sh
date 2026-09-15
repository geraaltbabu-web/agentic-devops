#!/usr/bin/env bash
set -euo pipefail
git --version
if git config --global --get user.name >/dev/null && git config --global --get user.email >/dev/null; then
  echo "global user.name and user.email are set (value not printed)."
else
  echo "Set user.name and user.email before real commits."
fi
