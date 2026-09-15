# Capstone — secure delivery environment

Design and demonstrate a small, synthetic web service on AWS. Stay free-tier-safe where possible; an architecture-only answer is acceptable for chargeable components.

## Requirements

- separate dev and production accounts in the target design
- three-AZ VPC design with public, private, and isolated subnet tiers
- private application compute behind an HTTPS load balancer
- managed database design with backups and Multi-AZ production option
- DNS, TLS, WAF, and DDoS considerations
- CI/CD authentication through OIDC
- immutable artifact in ECR
- Terraform remote-state design
- secrets stored outside source control
- CloudTrail, Config, GuardDuty, metrics, logs, traces, alarms, and runbooks
- scaling, deployment, rollback, backup restore, RTO, and RPO
- cost estimate, budget, tags, and cleanup

## Deliverables

1. Context and detailed architecture diagrams
2. Threat model and data classification
3. IAM trust and permission design
4. Network flow for client, deployment, application, database, and observability traffic
5. CI/CD stage design with gates and evidence
6. Infrastructure plan and sanitized validation output
7. Three failure drills and recovery evidence
8. Monthly cost estimate for dev and production
9. Destruction/cleanup checklist
10. Ten-minute technical presentation

## Required failure drills

1. Remove an application egress rule and diagnose the failed dependency
2. Deny one required IAM action and diagnose the exact policy layer
3. Deploy a failing health endpoint and prove automatic rollback

## Review rubric

- **Foundational:** identifies services and follows a tutorial
- **Working:** deploys safely and explains normal data/network flow
- **Proficient:** troubleshoots failures using evidence and least privilege
- **Advanced:** explains trade-offs, blast radius, recovery, cost, and governance
- **Expert:** designs reusable controls, anticipates failure modes, and teaches the reasoning clearly

You pass when another engineer can reproduce the design from your documentation, no secrets are exposed, cleanup is proven, and you can defend every service choice against at least one alternative.

## Suggested architecture (synthetic, not mandatory)

```text
User -> Route 53 -> ACM TLS on ALB (public subnets)
  -> target group: ECS/Fargate or ASG in private subnets
  -> RDS PostgreSQL in isolated subnets (design on paper if you skip paid RDS)
  -> S3 for objects via gateway endpoint
Logs -> CloudWatch Logs
Metrics -> CloudWatch alarms on 5xx and p99 latency
Audit -> CloudTrail to a log bucket (versioned, TLS-only)
Deploy -> GitHub Actions OIDC -> deploy role -> ECS update or Helm/Argo later
```

If a component costs money, **document it** and either skip live deploy or destroy within one hour.

## Step-by-step execution (sandbox)

1. Create a unique prefix, never reuse a public tutorial bucket name blindly
2. Deploy the course VPC or your own three-AZ design
3. Put a tiny static or container app behind TLS if you can stay cheap; otherwise stop at design plus CloudFormation VPC
4. Wire one alarm and prove it fires by breaking health
5. Record the three failure drills with CloudTrail event names (not full event JSON in Git)
6. Destroy stacks
7. Confirm Cost Explorer shows the expected drop the next day

## Presentation outline (10 minutes)

1. Problem and constraints (1 min)
2. Diagram and request path (2 min)
3. Identity and secrets (2 min)
4. Pipeline and promotion (2 min)
5. Failure drills and cost (2 min)
6. What you would add with a real budget (1 min)

## Anti-patterns that fail the capstone

- Access keys in GitHub secrets for a greenfield design
- Public RDS or public S3 “to make the demo work”
- Single AZ “because it is a lab” with no comment on production
- `latest` image tags
- No cleanup
- Copy-pasted account IDs into this public repository
