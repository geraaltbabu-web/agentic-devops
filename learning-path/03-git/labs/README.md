# Labs

Labs 0–5 are local. They create a throwaway repo under `/tmp` or `%TEMP%`.

```bash
cd learning-path/03-git/labs
chmod +x ./*.sh
./00-version.sh
./01-init-commit.sh
./02-branch-merge.sh
./03-protection-design.sh
./04-revert-not-reset.sh
./05-tag-release.sh
```

On Windows, run the same scripts in Git Bash.

## Lab 3 note

`03-protection-design.sh` prints a checklist. Fill it in your notes; it does not call GitHub APIs.

## Optional Lab 6 — GitHub (your account)

1. Create an empty **public or private** repo you own (not an employer org unless allowed).
2. Enable branch protection on `main`: PR required, no force push.
3. Push a branch, open a PR, merge via the UI.
4. Confirm you cannot push directly to `main`.

Do not store PATs in the repo.

## Completion gate

You can draw your last lab’s DAG, undo a bad commit on a shared branch with `revert`, and list five branch-protection settings.
