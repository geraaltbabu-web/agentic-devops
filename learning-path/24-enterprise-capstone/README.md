# 24 — Enterprise capstone

This is the last module. You combine **all** previous tools on a **synthetic** workload (reuse `banking-platform` as the reference implementation—do not copy employer systems).

## Scenario

A fictional payments API must run in **dev** and **prod** on AWS + OpenShift/ROSA (or EKS if you document the delta), with GitOps, CI, observability, and a 99.9% SLO.

## Deliverables (one pack)

1. Architecture diagram (network, identity, deploy path)
2. Account/OCP project layout
3. Git branching + protection + CODEOWNERS
4. CI (GitHub or GitLab or Jenkins)—OIDC, no static cloud keys
5. Image digest promotion
6. Terraform state split
7. Helm/Argo desired state
8. Secrets flow
9. Logging + metrics + three alerts + runbooks
10. DB backup/migration policy
11. Security gates
12. Cost estimate and kill switch
13. Game-day script (one failure)
14. 10-minute talk

## Constraints

- Synthetic data only
- Public Git must stay free of secrets and account IDs
- Prod apply is gated
- Rollback includes schema compatibility

## Pass bar

Another engineer can see how AWS, Linux, Git, YAML, Docker, K8s/OCP, Terraform, CI, Argo, ELK, Prom, and Vault-or-SM fit **one** path—not 24 disconnected tools.

## Suggested order of work

Follow modules 01→23 notes. Fill gaps by reading this repo’s `banking-platform/` and `learning-path/01-aws-cloud/` through `23-platform/`.
