# Git in the DevOps stack

Git is the **desired-state bus**. Almost every later module plugs in here.

## AWS

CI checks out a SHA, assumes a role via OIDC, deploys that SHA’s artifact. CloudTrail + Git SHA + image digest.

## Linux / Ansible

Playbooks and cloud-init templates live in Git. Tags are how you know which host baseline shipped.

## Docker

`LABEL org.opencontainers.image.revision=$GIT_SHA`. Build from SHA, not dirty worktree, in CI.

## Kubernetes / Helm / OpenShift

Manifests and values in Git. Promotion = merge to an env branch or folder. Argo CD watches Git.

## Terraform

Modules and live env folders in Git. Plan on PR; apply on merge to a protected branch. State is **not** in Git.

## Jenkins / GitLab CI / GitHub Actions

The pipeline definition is Git. Branch protection requires those pipelines. Jenkinsfiles in Git, not only on the master disk.

## ELK / Prom-Grafana

Dashboard JSON and alert rules as code in Git (or Grafana Git sync). Avoid “someone clicked Save” as the only copy.

## Secrets

Git is the wrong store. Sealed secrets / SOPS / Vault / cloud secret managers. Pre-commit and server-side scanning.

## Mental picture

```text
Human -> branch -> PR/MR -> required checks -> merge to main
  -> build SHA
  -> GitOps commit or CD job
  -> cluster / cloud
```

If a change is not in Git, it will not survive the next incident.
