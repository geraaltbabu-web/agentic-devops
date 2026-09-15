# Remotes, GitHub, GitLab, and protection

## Remotes

```bash
git remote -v
git fetch origin
git status -sb
```

`fetch` updates remote-tracking branches (`origin/main`). `pull` is fetch + merge or rebase (see `pull.rebase`). Prefer **fetch then rebase** until you know the default.

`push -u origin HEAD` sets upstream once.

`origin` is a convention, not magic. `upstream` often means the parent of a fork.

## Authentication

- HTTPS + credential helper / SSO
- SSH keys (ed25519) with a passphrase
- Fine-grained PATs: least privilege, expiry
- **Never** put a PAT in the repo, a screenshot, or a training video

CI: OIDC to cloud (module 01); deploy keys or job tokens for Git, scoped to the repo.

## GitHub vs GitLab (operator map)

| Job | GitHub | GitLab |
|-----|--------|--------|
| Change request | Pull request | Merge request |
| Protect branch | Rulesets / branch protection | Protected branches |
| Required CI | Required status checks | Pipelines must succeed |
| Env approvals | Environments | Protected environments |
| Permissions | Teams + roles | Groups + roles |
| CI YAML | `.github/workflows` | `.gitlab-ci.yml` |
| Package registry | ghcr / packages | GitLab registry |
| Issue/board | Issues / Projects | Issues / boards |

Learn both maps. Enterprises run **both**.

## Protection rules you should be able to recite

For `main` / `master` / `release/*`:

- No direct push
- PR/MR required
- Required checks (lint, test, secret scan)
- Require up-to-date branch before merge (optional but common)
- CODEOWNERS for sensitive paths
- Linear history **or** merge commits—pick one, document it
- Admin bypass: auditable, rare
- Signed commits if policy says so (GPG/SSH signing)

Production deploy: **environment protection** + required reviewers. Git is not the only gate; it is the first.

## Fork vs shared clone

Inner-source: developers push branches on the same repo. Forks: open source or strong isolation. Permissions differ (workflow `pull_request` from forks cannot access secrets the same way). Know that before you copy a GitHub Actions pattern.

## Checkpoint

Why can a GitHub Action on `pull_request` from a fork not receive repository secrets by default?
