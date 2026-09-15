# Command cookbook

Safe defaults: inspect first.

```bash
git --version
git status -sb
git log --oneline --decorate -n 15
git log --oneline --graph --all -n 20
```

## Daily

```bash
git fetch origin
git switch main
git merge --ff-only origin/main   # or: git rebase origin/main
git switch -c feat/example
git add path/to/file
git diff --staged
git commit -m "Explain why."
git push -u origin HEAD
```

## Undo (uncommitted)

```bash
git restore path
git restore --staged path
```

## Undo (committed, not pushed)

```bash
git reset --soft HEAD~1
```

## Undo (pushed to shared main)

```bash
git revert HEAD
git push
```

## Inspect remotes

```bash
git remote -v
git branch -vv
git show origin/main
```

## Tags

```bash
git tag -l
git show v1.0.0
```

## Ignore debug

```bash
git check-ignore -v .env
```

## Bisect sketch

```bash
git bisect start
git bisect bad
git bisect good v1.0.0
# run test; git bisect good|bad
git bisect reset
```
