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
