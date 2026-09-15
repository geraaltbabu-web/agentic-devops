# Glossary and service map

## Glossary

| Term | Meaning |
|------|---------|
| Account | Billing, quota, and IAM blast-radius boundary |
| Region | Geographic API and data-residency boundary |
| AZ | Isolated infrastructure location inside a Region |
| ARN | Amazon Resource Name |
| Control plane | APIs that create/change resources (mostly CloudTrail) |
| Data plane | Traffic that serves customers (VPC flow, app logs) |
| Idempotent | Repeating the same request does not create extra side effects |
| Least privilege | Only the actions and resources required |
| OIDC | Token-based federation; CI assumes a role without static keys |
| Promotion | Same artifact moves env to env; not rebuilt |
| RTO | Time to restore service |
| RPO | Maximum tolerable data loss |
| SCP | Organization guardrail; cannot grant permissions |
| Shared responsibility | AWS secures the cloud; you secure your config and data |

## Service map by DevOps job

| Job | AWS services |
|-----|----------------|
| Identity | IAM, Identity Center, STS, Organizations, KMS |
| Network | VPC, SG, NACL, IGW, NAT, endpoints, Route 53, TGW |
| Compute | EC2, ASG, Lambda, ECS, EKS, ROSA |
| Traffic | ALB, NLB, API Gateway, CloudFront, WAF, Shield |
| State | S3, EBS, EFS, RDS, DynamoDB, ElastiCache |
| Delivery | Code artifacts in ECR, CodePipeline optional, or GitHub/GitLab/Jenkins + OIDC |
| Config as code | CloudFormation, CDK, Terraform (module 12) |
| Observe | CloudWatch, CloudTrail, X-Ray, Config, Managed Prometheus/Grafana |
| Secure | GuardDuty, Security Hub, Inspector, Secrets Manager, Macie |
| Operate | Systems Manager, Backup, Autoscaling, Budgets |

## What this module does **not** replace

- Linux internals (module 02)
- Writing production Dockerfiles (module 07)
- Cluster day-2 operations (modules 08–10)
- Terraform state design in depth (module 12)
- Jenkins/GitLab/Argo syntax in depth (modules 14–16)
- ELK and Prom/Grafana dashboards in depth (modules 18–19)

AWS is the **substrate**. The rest of the path teaches the tools that run on it.
