# Foundations: objects, commits, refs

## Mental model

Git stores **snapshots**, not deltas you have to think about daily.

```text
working tree  ->  index (staging)  ->  commit object
```

A **commit** points to a tree (directories/files) and zero or more parents. A **branch** is a movable name pointing at a commit. **HEAD** is “where I am” (usually a branch name).

```text
main:    A---B---C
              \
feature:       D---E   <- HEAD
```

Detached HEAD: HEAD points at a commit, not a branch. Fine for inspect; dangerous for new work unless you create a branch immediately.

## The three trees

| Tree | Command that changes it |
|------|-------------------------|
| Working directory | edit files, `git restore` |
| Index | `git add`, `git restore --staged` |
| HEAD commit | `git commit`, `git reset` |

`git status` is how you know which tree is dirty. Read it every time.

## Identity and commit messages

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Use a real identity you are allowed to publish. This course repo is public.

Message convention (good enough for enterprises):

```text
Short imperative summary (≤72 chars)

Why this change exists.
What would break if we revert it.
```

`fix stuff` is not a message. Conventional Commits (`feat:`, `fix:`) help changelog tools; they are optional unless your team requires them.

## Inspect, do not memorize hashes

```bash
git log --oneline --decorate --graph --all
git show HEAD
git diff
git diff --staged
```

Hashes can be abbreviated uniquely. Tags and branches are for humans.

## `.gitignore` is a control

Ignore: `.env`, `*.tfstate`, `venv/`, `node_modules/`, IDE junk, secrets, OS files.

`git add -f` bypasses ignore. That is a smell in review.

`git check-ignore -v path` explains why a file is ignored.

## Checkpoint

Without notes: difference between `restore`, `reset --mixed`, and `revert`. (You will confirm in chapter 4.)
