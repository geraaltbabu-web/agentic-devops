# 01 — AWS Cloud for enterprise DevOps

Goal: go from a new AWS sandbox to the level of a junior-to-mid platform engineer who can design, deploy, observe, secure, cost-control, and troubleshoot AWS in an enterprise delivery stack.

This module is **theory + labs + enterprise patterns + failure drills + interview Q&A**. Later modules (Linux, Docker, OpenShift, GitLab, Jenkins, Argo CD, ELK, Prometheus/Grafana, Terraform) assume you finished this one.

## Before you begin

Use a **personal sandbox account only**. Never use an employer, customer, or production account.

You need:

- MFA on the root user
- AWS CLI v2, Git, Python 3.12+, and an editor
- A monthly budget with email alerts at a low threshold
- Willingness to **delete every lab resource** in the same session

Optional later: GitHub Actions in this public repo, Terraform CLI, `jq`.

> AWS pricing and free-tier terms change. Recheck pricing before any lab that creates compute, NAT, load balancers, databases, or OpenSearch. This course avoids NAT Gateway, RDS, OpenSearch, and always-on EC2 in the default labs.

## How to study

| Mode | What to do |
|------|------------|
| Read | Work chapters in order. Draw every diagram on paper. |
| Lab | Run the matching lab the same day. Write a 5-line post-lab note: what, why, failure, fix, cleanup. |
| Speak | Answer the Q&A out loud before reading the model answer. |
| Prove | Finish the capstone without copying a tutorial blindly. |

Suggested pace: **10–14 days**, 90–120 minutes per day. A weekend crash course is possible; retention will be worse.

## Learning sequence

0. [Study plan and competency rubric](00-study-plan.md)
1. [Foundations, IAM, CLI, and how AWS actually authorizes requests](01-foundations.md)
2. [Networking, compute, storage, data, and observability services](02-core-services.md)
3. [Enterprise DevOps: accounts, OIDC CI/CD, GitOps, Terraform, containers](03-enterprise-devops.md)
4. [Operations, security, reliability, incidents, and cost](04-operations.md)
5. [Real-world questions and answers](05-real-world-q-and-a.md)
6. [CLI cookbook](06-cli-cookbook.md)
7. [Glossary and service map](07-glossary.md)
8. [How AWS connects to Linux, Docker, OCP, Git, CI, ELK, and Terraform](08-aws-in-the-devops-stack.md)
9. [Hands-on labs](labs/README.md)
10. [Capstone](capstone.md)

## What “expert enough for this module” means

You can, without notes, do all of the following:

- Name the caller, Region, action, resource, and policy layer that caused an `AccessDenied`
- Sketch a three-AZ VPC with public / private / isolated tiers and explain every hop
- Choose EC2 vs ECS vs EKS/ROSA vs Lambda and defend the choice
- Design S3, RDS, and DynamoDB usage with backup, encryption, and IAM
- Describe a GitHub/GitLab/Jenkins → OIDC → IAM role → deploy path with no static keys
- Diagnose ALB 502, private-subnet “no internet”, noisy CloudWatch, and a surprise bill
- Write a rollback plan that includes schema compatibility and health checks

## Lab safety rules

1. One sandbox Region. Default `us-east-1`.
2. Tag everything: `Project=devops-mastery`, `Owner=<you>`, `Expires=<YYYY-MM-DD>`.
3. `aws sts get-caller-identity` before every change.
4. Review templates and plans before apply.
5. Never commit credentials, account IDs, private keys, SSO tokens, or Terraform state.
6. Cleanup in the same sitting. Prefer CloudFormation delete over leftover console clicks.
7. Open Cost Explorer after every session.

## Evidence of completion (keep private)

Keep notes locally. Do **not** push:

- Access keys, tokens, cookies, MFA seeds
- Account IDs, user ARNs, bucket names that include your account
- Console screenshots with billing or identity
- `~/.aws/` files

You may push: diagrams with fake names, sanitized command shapes, architecture decisions, and answers to the scenario questions.

## Public-repo rule

This folder is designed to stay public. If you add your own lab output, scrub it first.
