#!/usr/bin/env bash
set -euo pipefail

cat <<'EOF'
Design a protection policy for main (write answers in your notes):

1. Who may push? (nobody except automation with a break-glass path)
2. Required status checks (name three: unit test, secret scan, IaC lint)
3. CODEOWNERS for /infra and /deploy
4. Environment name for production deploys and who approves
5. Whether squash is allowed and why
6. What happens on Friday 16:00 freeze

Compare GitHub branch protection vs GitLab protected branches using chapter 3.
EOF
