# Real-world questions and answers

Answer aloud. Mention **verification** and **who can see the history**.

## Foundations

**What does a commit store?**  
A snapshot (tree), parent(s), author, message. Not “a diff” as the primary object.

**index vs working tree?**  
Index is what the next commit will contain. `git add` copies from working tree to index.

**Why not `git add .` by habit?**  
You will add secrets, binaries, and generated files. `git status` then add paths.

## Branching

**Merge or rebase for a shared feature branch?**  
Merge or PR squash. Rebase only if you are the only one using the branch or you coordinate a force-push.

**Squash merge downside?**  
You lose the ability to bisect inside the feature. Fine if the squash message is precise.

**Hotfix on prod while feature is open?**  
Branch from the release tag/commit, PR to `main`, cherry-pick or merge back so `main` is not behind prod.

## Forges

**Protected branch still got a bad commit.**  
Admin bypass, compromised account, or required checks that did not actually test the change. Audit the merge and the bypass log.

**Fork PR and secrets.**  
GitHub does not give fork PRs write secrets on `pull_request`. Use `pull_request_target` only if you understand the injection risk (untrusted code with secrets). Prefer not to.

**GitLab vs GitHub CI file?**  
`.gitlab-ci.yml` vs `.github/workflows/*.yml`. Same idea: YAML, jobs, rules, artifacts.

## Incidents

**Undo a merge on `main` that is already in prod?**  
`git revert -m 1 <merge-sha>` (understand `-m 1`) plus a deploy of that revert, or a forward fix. Communicate. Do not reset origin/main.

**Secret committed and pushed.**  
Rotate, revoke, scan forks/logs, then history purge if required. Ignore-file-only is not enough.

**Lost commits after reset --hard.**  
`git reflog`. Recover. Then stop using hard reset on shared branches.

## GitOps / releases

**Why tag the image with Git SHA?**  
Immutable link from cluster back to source. `latest` is not a version.

**Two tools apply the same Helm chart.**  
Drift. One mutator per environment.

## Self-score

If you cannot explain revert vs reset without notes, restudy chapter 4.
