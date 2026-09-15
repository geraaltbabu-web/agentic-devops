# State and CI

State = mapping to real objects. S3 + lock. Encryption. No local state for teams.

PR: `plan`. Merge to env branch: `apply`. OIDC role. `-out=tfplan` and apply that file so plan≠apply drift.

Import and moved blocks for refactor. Never hand-edit state first.
