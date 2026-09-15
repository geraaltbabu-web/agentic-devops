# 03 — Git, GitHub, and GitLab for enterprise DevOps

Goal: treat Git as the system of record for code, IaC, and GitOps—not as “save files.” After this module you can run a trunk-based or short-lived-branch workflow, review a merge request like a platform team, protect `main`, and recover from the mistakes that actually happen on Friday.

GitHub and GitLab are **forges** (hosting + permissions + CI + PRs/MRs). The object model is still Git.

## Before you begin

- Git 2.40+ (`git --version`)
- A **personal** GitHub and/or GitLab account (this public repo is fine to fork; do not use an employer account for labs that rewrite history)
- Module 02 Bash habits: quote variables; do not paste tokens into the shell history if you can avoid it

Never force-push a shared branch. Never `git add .` in a folder that might contain `.env` or keys.

## Learning sequence

0. [Study plan](00-study-plan.md)
1. [Foundations: objects, commits, refs](01-foundations.md)
2. [Daily workflow: branch, review, integrate](02-branching-and-review.md)
3. [Remotes, GitHub, GitLab, protection](03-forges-and-protection.md)
4. [History surgery, incidents, and secrets](04-history-and-incidents.md)
5. [Releases, GitOps, and CI identity](05-releases-and-gitops.md)
6. [Real-world Q&A](06-real-world-q-and-a.md)
7. [Command cookbook](07-cli-cookbook.md)
8. [Git in the DevOps stack](08-git-in-the-devops-stack.md)
9. [Labs](labs/README.md)
10. [Capstone](capstone.md)

## Competency checkpoints

- Draw a commit DAG and explain `HEAD`, branch, tag
- Choose merge vs rebase vs squash for a given policy
- Open a PR/MR with a test plan; review for blast radius, secrets, and rollback
- Explain branch protection, CODEOWNERS, required checks, and environments
- Recover a deleted branch with reflog; revert a bad merge without rewriting `main`
- Describe what to do if a secret was committed
- Map Git refs to Argo CD, Jenkins, GitLab CI, and Terraform

## Safety

1. Labs 1–5 are **local** (temp directories). They do not need a network.
2. Optional Lab 6 uses GitHub on a throwaway repo you own.
3. Do not run `reset --hard` or `push --force` on `main` of a shared repo.
4. Do not commit credentials. If you do, rotate first; then rewrite or purge with a documented process.
