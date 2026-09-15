# 01 — AWS Cloud for enterprise DevOps

Goal: progress from a new AWS account to confidently operating secure, observable, cost-aware AWS environments and integrating them with a delivery platform.

## Before you begin

You need:

- A personal AWS sandbox account—never use an employer or production account
- MFA on the root user
- AWS CLI v2, Git, Python 3.12+, and an editor
- A budget alert; labs avoid NAT Gateway, paid databases, and long-running compute

> AWS pricing and free-tier terms change. Check the AWS pricing page before every lab. Cleanup is mandatory.

## Learning sequence

1. [Foundations and setup](01-foundations.md)
2. [IAM, networking, compute, storage, and databases](02-core-services.md)
3. [Enterprise DevOps integration](03-enterprise-devops.md)
4. [Operations, security, reliability, and cost](04-operations.md)
5. [Real-world questions and answers](05-real-world-q-and-a.md)
6. Complete the [hands-on labs](labs/README.md)
7. Complete the [capstone](capstone.md)

## Competency checkpoints

After this module you should be able to:

- Explain Regions, Availability Zones, the shared responsibility model, and AWS API behavior
- Secure an account with IAM Identity Center, roles, temporary credentials, MFA, and least privilege
- Design a three-tier VPC and reason about routes, security groups, NACLs, DNS, and endpoints
- Select EC2, ECS, EKS, Lambda, or managed services based on operational trade-offs
- Choose S3, EBS, EFS, RDS, DynamoDB, or ElastiCache for a workload
- Use CloudTrail, CloudWatch, Config, GuardDuty, KMS, Secrets Manager, and Systems Manager
- Build an enterprise CI/CD path using OIDC instead of permanent AWS keys
- Diagnose common reachability, IAM, instance, deployment, and cost failures
- Design backup, multi-AZ, autoscaling, recovery, and safe change strategies

## Lab safety rules

1. Use one sandbox Region, default `us-east-1`.
2. Tag every resource: `Project=devops-mastery`, `Owner=<you>`, `Expires=<date>`.
3. Run `aws sts get-caller-identity` before every change.
4. Review generated plans/templates before deployment.
5. Never commit credentials, account IDs, private keys, or state files.
6. Run cleanup immediately after each lab.
7. Check Cost Explorer and Budgets after lab sessions.

## Evidence of completion

Keep only non-sensitive evidence in your own notes:

- Architecture decisions and diagrams
- Sanitized command output
- Failure symptoms, root causes, and fixes
- Cost estimate and cleanup proof
- Answers to the scenario questions

Do not copy access keys, tokens, account IDs, resource ARNs, or console screenshots containing private details.
