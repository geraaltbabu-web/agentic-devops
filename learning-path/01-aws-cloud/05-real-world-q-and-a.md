# Real-world questions and answers

Answer aloud before expanding your written answer. A strong answer states assumptions, trade-offs, verification, security, cost, and rollback.

## Foundations

**Why use multiple AWS accounts instead of only multiple VPCs?**  
Accounts provide stronger IAM, quota, billing, logging, and blast-radius isolation. VPCs primarily isolate networking.

**Region or Availability Zone?**  
A Region is a geographic API boundary. An AZ is an isolated infrastructure location inside a Region. Multi-AZ handles localized failures; multi-Region addresses larger failures with much higher complexity.

**Why avoid IAM users?**  
They commonly rely on long-lived credentials. Federation, SSO, instance/task/pod roles, and OIDC provide temporary, scoped, auditable sessions.

## Networking

**A private EC2 instance cannot download packages. What do you check?**  
DNS, subnet route to NAT or relevant VPC endpoints, NAT placement and public route, security group egress, NACL return ports, proxy settings, and source/destination behavior. Avoid giving the instance a public IP as a quick fix.

**Security group versus NACL?**  
Security groups are stateful and attached to resources; NACLs are stateless subnet controls. Most application policy belongs in security groups.

**Why can a healthy application still fail ALB health checks?**  
Wrong path/port/protocol, application bound only to localhost, security group path blocked, host-header behavior, timeout, status code mismatch, or insufficient startup grace.

## Compute and containers

**EC2, ECS, EKS, or Lambda?**  
Choose from runtime constraints, portability, scaling model, team expertise, compliance, operational ownership, and cost. Kubernetes is not automatically the enterprise answer.

**How do you deploy without downtime?**  
Multiple healthy replicas across AZs, readiness checks, capacity surge, connection draining, backward-compatible schemas, progressive traffic, metric gates, and tested rollback.

**Why tag images with a commit SHA instead of `latest`?**  
Immutable references make promotion, audit, rollback, and incident diagnosis deterministic.

## Data

**Does Multi-AZ RDS eliminate backups?**  
No. Multi-AZ improves availability. Backups protect against deletion, corruption, application mistakes, and recovery to an earlier point.

**How do you avoid duplicate SQS processing?**  
Assume at-least-once delivery. Use idempotency keys, conditional writes/transactions, bounded retries, visibility timeout management, and a dead-letter queue.

**How do you deploy a breaking database change?**  
Use expand/contract: add compatible schema, deploy code that handles both versions, migrate data, verify, remove old usage, then remove old schema later.

## IAM and security

**A role policy allows S3 GetObject but access is denied. Why?**  
Possible explicit deny in SCP, permission boundary, session policy, bucket policy, VPC endpoint policy, or KMS key policy; wrong object ARN, account, or Region; or request conditions not met.

**How should CI authenticate to AWS?**  
OIDC federation to a narrowly trusted role with temporary credentials. Restrict claims to repository/project, protected branch or environment, and intended audience.

**How do you prevent secrets entering logs?**  
Structured logging with allowlisted fields, centralized redaction, code review, secret scanning, restricted log access, and tests using canary secrets. Do not depend on developers remembering.

## Observability and incidents

**CPU is normal but latency is high. What next?**  
Check request rate, saturation elsewhere, dependency latency, connection pools, queues, locks, DNS, network errors, throttling, GC/runtime pauses, traces, and recent changes.

**CloudWatch alarm is noisy. How do you improve it?**  
Tie it to user impact, adjust period/evaluation windows, handle missing data, use percentiles or anomaly detection where appropriate, combine symptoms, and link a runbook.

**What is your first action during an incident?**  
Establish impact and stabilize service. Root-cause analysis follows after mitigation unless diagnosis is required to choose a safe mitigation.

## Cost and governance

**Why is a NAT Gateway bill unexpectedly high?**  
Hourly gateways plus per-GB processing, often multiplied by cross-AZ routing. Use one NAT per AZ for resilience, same-AZ routes, VPC endpoints, caching, and traffic analysis; cost and resilience trade off.

**How do you stop abandoned sandbox resources?**  
Separate sandbox accounts, mandatory owner/expiry tags, budgets, scheduled shutdown, policy controls, inventory reports, and automated cleanup with exception handling.

## Practical interview round

Design verbally:

1. A highly available public API with private application and database tiers
2. A secure GitHub Actions deployment using OIDC
3. Central logs from 20 accounts
4. A recovery plan with RTO 30 minutes and RPO 5 minutes
5. A migration from manually managed EC2 to containers

For each, cover architecture, identity, network path, data, observability, failure behavior, cost, deployment, rollback, and evidence.

## Extra enterprise questions

**What is the difference between a task role and a task execution role on ECS?**  
Execution role: pull images, write logs, retrieve secrets at start. Task role: what the app code can do at runtime (S3, SQS). Mixing them is a common over-privilege.

**How do you give an EKS pod S3 access?**  
IRSA or EKS Pod Identity: a Kubernetes service account mapped to an IAM role with a trust policy constrained to the OIDC issuer and service account. Do not put access keys in a Secret.

**When is CloudFront in front of an ALB justified?**  
Global cache, TLS at edge, WAF, DDoS, and cheaper egress for static/cacheable content. Skip it for a purely internal API.

**How do you rotate an RDS password used by 20 tasks?**  
Store in Secrets Manager, enable rotation, grant the task role `GetSecretValue` on that ARN, restart or refresh clients, never bake the password into the image.

**A Terraform apply failed mid-way. What now?**  
Read state vs real resources, do not hand-edit state first, `plan` again, fix the API error (IAM, quota, dependency), consider `refresh`. If the state lock is stuck, confirm no other apply is running before unlocking.

**Why might `aws s3 cp` work while an app using a role fails?**  
Your CLI uses a different principal (SSO admin) than the app role. Always reproduce with the app role via `sts assume-role` or the instance profile.

**How do you restrict console access to one Region?**  
IAM condition `aws:RequestedRegion` plus optional SCP. Remember global services still need careful exceptions.

**What is a permission boundary used for?**  
To let a team create roles without being able to create a role more powerful than the boundary. Platform teams use this for self-service.

**Canary vs blue/green on AWS?**  
Canary: small % of traffic, watch metrics, increase. Blue/green: two environments, flip. CodeDeploy, ALB weighted target groups, or service mesh can implement either. Choose based on extra cost vs faster rollback.

**How do you prove encryption at rest for S3?**  
Bucket default encryption, object metadata `ServerSideEncryption`, KMS key policy, CloudTrail, and a Config rule. A screenshot of a checkbox is weak evidence.

**What do you do when GuardDuty fires `UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration`?**  
Treat as incident: disable keys/roles, rotate, isolate instance, review CloudTrail, check IMDS hop limit and SSRF, rebuild the host from a clean AMI.

**Why are VPC flow logs not the first tool?**  
They are sampled or high-volume and cost money. Start with SG rules, routes, and application errors; use flow logs when those are exhausted.

**How should non-prod differ from prod?**  
Same architecture, smaller size, scheduled stop, weaker (but not public) data, cheaper logging retention, still no long-lived keys. Drift in architecture teaches the wrong muscle memory.

**What is the blast radius of `Resource: "*"` on `iam:PassRole`?**  
The principal can pass any role the account allows, including admin, to EC2/Lambda. Always constrain `PassRole` to explicit role ARNs and `iam:PassedToService`.

## Self-score

Give yourself 1 point per question you answered with: identity, verification, security, cost, and rollback. Below 12/20: restudy chapters 1–4. 12–16: proficient. 17+: ready for the capstone presentation.
