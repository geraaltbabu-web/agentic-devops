# Study plan and competency rubric

## Two-week plan

### Days 1–2 — Account and identity

Read [01-foundations.md](01-foundations.md). Labs 0 and 1.

Exit ticket: you can explain shared responsibility, SSO vs access keys, and `sts get-caller-identity` output fields (`Account`, `Arn`, `UserId`).

### Days 3–5 — Core building blocks

Read [02-core-services.md](02-core-services.md). Labs 2–5.

Exit ticket: you can draw a VPC, explain why private subnets have no default internet, and write an S3 bucket policy that requires TLS.

### Days 6–8 — Delivery platform on AWS

Read [03-enterprise-devops.md](03-enterprise-devops.md) and [08-aws-in-the-devops-stack.md](08-aws-in-the-devops-stack.md). Lab 7 (OIDC design, no live CI required).

Exit ticket: you can describe OIDC claims, a deployment role, ECR immutable tags, and why production is a promotion not a rebuild.

### Days 9–11 — Operate it

Read [04-operations.md](04-operations.md) and [06-cli-cookbook.md](06-cli-cookbook.md). Lab 8 (alarms) and optional Lab 6 (EC2/SSM).

Exit ticket: you can run an incident tabletop: detect, mitigate, verify, communicate, prevent.

### Days 12–14 — Prove it

Answer [05-real-world-q-and-a.md](05-real-world-q-and-a.md) out loud. Complete [capstone.md](capstone.md).

## Rubric

| Level | Signal |
|-------|--------|
| Following a tutorial | Resources exist; you cannot explain a failure |
| Working | You deploy, tag, and clean up; you explain happy path |
| Proficient | You use CloudTrail/IAM/VPC flow reasoning; least privilege |
| Advanced | You design multi-account, OIDC, rollback, cost, and RTO/RPO |
| Teaching | Another engineer can reproduce from your notes without secrets |

Stay on a chapter until you can teach it. Speed without diagnosis is not DevOps.

## Daily lab hygiene

```text
1. Identity check
2. Create with tags
3. Prove with a read API
4. Break one control on purpose (SG, IAM, health)
5. Fix using evidence
6. Delete
7. Confirm Cost Explorer
```
