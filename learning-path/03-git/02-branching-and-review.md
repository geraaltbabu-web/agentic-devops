# Daily workflow: branch, review, integrate

## Default enterprise shape

**Trunk-based with short-lived branches** is the usual DevOps default:

1. Update `main` (`git fetch` + `git rebase origin/main` or merge)
2. Branch `feat/short-name` or `fix/ticket-123`
3. Small commits; push; open PR/MR
4. CI must pass; one or two reviewers
5. Squash or merge per team policy
6. Delete the branch

Long-lived `develop` + Git Flow is heavier. Use it only if release trains require it. Do not invent a third model.

## Merge vs rebase vs squash

| Method | Result on `main` | Use |
|--------|------------------|-----|
| Merge commit | Extra merge node; full history | Preserve exact branch topology |
| Squash | One commit on `main` | Noisy feature branches |
| Rebase then fast-forward | Linear history | Local cleanup **before** share |

**Never rebase commits already on a shared branch** unless the whole team agrees (almost never for `main`).

Conflict resolution: understand both sides; run tests; do not “accept theirs” blindly on IAM or Helm.

## Review like a DevOps engineer

Look for:

- Secrets, account IDs, internal hostnames
- `chmod 777`, `latest` tags, `curl | sudo bash`
- Terraform/state, kubeconfigs
- Missing rollback or expand/contract for data
- CI that uses static cloud keys
- Scope: is this one change or five?

A review without running the test plan is theater.

## CODEOWNERS

Maps paths to reviewers (`*.tf @platform`, `/deploy/ @sre`). Protection rules can require owner approval. Keep the file small or it becomes rubber-stamping.

## PR/MR hygiene

- Description: why, how to test, risk, rollback
- Link the change ticket
- Draft until CI is green if your forge supports it
- Do not `@everyone`

GitHub: Pull Request. GitLab: Merge Request. Same social contract.

## Checkpoint

When is squash the wrong policy? (Hint: you need to bisect a 40-commit feature that was squashed to one “WIP”.)
