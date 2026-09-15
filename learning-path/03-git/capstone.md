# Capstone — branching policy you could run a team on

Write a one-page standard for a synthetic service (`payments-api`):

1. Branch naming
2. How `main` is protected (GitHub *and* GitLab wording)
3. Required checks
4. CODEOWNERS
5. Release tagging and how the image tag is formed
6. Hotfix path
7. Secret-push response
8. Who may force-push (hopefully nobody on `main`)

## Prove it locally

Using the lab scripts as a template, create a repo that:

- Has a merge or a conflict resolution you can explain
- Uses `git revert` to undo a bad commit
- Has an annotated tag

Paste only **sanitized** `git log --oneline --graph` into your notes (no employer remotes).

## Pass bar

A new teammate can follow the standard without asking which button is “squash.”
