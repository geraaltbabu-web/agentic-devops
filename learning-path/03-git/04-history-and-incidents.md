# History surgery, incidents, and secrets

## reset vs revert vs restore

| Command | Typical use | Rewrites published `main`? |
|---------|-------------|----------------------------|
| `git restore` | Throw away uncommitted edits | No |
| `git reset --soft` | Uncommit, keep index | Only if you push force |
| `git reset --mixed` | Uncommit, unstage | Same |
| `git reset --hard` | Destroy uncommitted + commit pointer | Dangerous |
| `git revert` | New commit that undoes an old one | **No** — this is the prod-safe undo |

On shared `main`, **revert** (or a forward fix). Do not reset.

## reflog

```bash
git reflog
git switch -c rescue HEAD@{2}
```

Reflog is local (default ~90 days). It saves you from “I reset the wrong thing.” It is not a backup of the server.

## cherry-pick and bisect

- Cherry-pick: copy a commit onto another branch (conflicts possible; duplicate hashes if misused)
- `git bisect`: binary search for the commit that broke tests

## Submodules and subtrees

Prefer a monorepo or separate repos with versioned packages. Submodules surprise CI and juniors. If you inherit them, learn `submodule update --init --recursive`.

## Secret in Git

Assume the secret is **compromised** the moment it is pushed, even to a “private” repo.

1. Rotate the credential (IAM key, token, password)
2. Revoke the old one
3. Purge from history if policy requires (`git filter-repo` / BFG) **and** force-push with coordination
4. Scan all forks and CI logs
5. Add pre-commit secret scanning and a server-side scan
6. Post-incident: how it entered (`git add .`, sample env file)

`.gitignore` after the fact does not remove history.

## Force push

`git push --force-with-lease` is less bad than `--force` (refuses if remote moved). Still forbidden on protected `main`.

## Checkpoint

A coworker force-pushed `main` and your local commits vanished from the branch. What two places do you look first?
