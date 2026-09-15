# Core services and design decisions

## Networking

A typical enterprise VPC spans three Availability Zones:

```text
Internet
  -> Route 53 / CloudFront / WAF
  -> public load balancer subnets
  -> private application subnets
  -> isolated database subnets
```

Key components:

- **Route table:** determines the next hop; most connectivity failures are route or policy failures
- **Internet Gateway:** public IPv4 connectivity for resources with public addresses
- **NAT Gateway:** outbound internet for private subnets; resilient but chargeable
- **VPC endpoint:** private path to AWS services; gateway endpoints for S3/DynamoDB, interface endpoints for many others
- **Security group:** stateful resource firewall; allow rules only
- **NACL:** stateless subnet firewall; allow and deny rules; ephemeral return ports matter
- **Route 53:** public/private DNS and health-aware routing
- **Transit Gateway:** hub for many VPCs and on-premises networks

Troubleshoot connectivity layer by layer: DNS → route → security group → NACL → listener → target health → application.

## Compute choice

- **EC2:** maximum control; you patch OS, agents, scaling, and images
- **Auto Scaling Group:** replaces unhealthy instances and scales EC2 fleets
- **Lambda:** event-driven short tasks; watch limits, cold starts, retries, and idempotency
- **ECS/Fargate:** AWS-native containers with less cluster administration
- **EKS:** Kubernetes portability and ecosystem with higher operational complexity
- **ROSA:** managed OpenShift on AWS with Red Hat platform features

Selection question: what operational responsibility does the team genuinely need to own?

## Load balancing and scaling

- ALB: HTTP/HTTPS, host/path routing, WAF integration
- NLB: TCP/UDP/TLS, static IPs, very high throughput
- GWLB: virtual network appliances
- Target tracking policies are usually safer than hand-built threshold chains
- Scale on a workload signal: request count, queue depth, concurrency, or latency—not CPU by default

## Storage

- **S3:** durable object storage; versioning, lifecycle, replication, object lock
- **EBS:** block storage for one AZ; snapshot for backup
- **EFS:** managed shared NFS across AZs
- **FSx:** managed specialized filesystems

S3 enterprise baseline: block public access, TLS-only bucket policy, KMS encryption where required, versioning, lifecycle, access logging, ownership tags.

## Databases and messaging

- **RDS/Aurora:** relational transactions, Multi-AZ availability, snapshots, read replicas
- **DynamoDB:** key/value access at scale; partition-key design is critical
- **ElastiCache:** cache/session/fast ephemeral data; never the only system of record
- **SQS:** durable queue; at-least-once delivery means consumers must be idempotent
- **SNS:** pub/sub fan-out
- **EventBridge:** event routing and integration
- **Kinesis/MSK:** streaming platforms

Backups are not proven until restore tests pass. Multi-AZ is availability, not a substitute for backup.

## Identity, encryption, and secrets

- KMS protects data keys and enforces cryptographic access
- Secrets Manager stores and rotates application secrets
- Parameter Store holds configuration and lower-complexity secure parameters
- ACM provisions certificates for supported AWS services
- Systems Manager replaces many SSH-based operational workflows

Applications on AWS should use instance, task, Lambda, or pod roles. Never inject static AWS keys into images or Kubernetes Secrets.

## Observability and audit

- CloudWatch Metrics, Logs, Alarms, dashboards, and Container Insights
- CloudTrail records control-plane and selected data events
- AWS Config records configuration and evaluates compliance
- X-Ray/OpenTelemetry provides distributed traces
- GuardDuty detects suspicious activity
- Security Hub aggregates findings

An actionable alert includes impact, threshold, duration, owner, dashboard, and runbook. Alert on user-visible symptoms and exhaustion trends, not every transient event.

## Service selection exercise

For each workload, document:

1. traffic and latency
2. consistency and durability
3. availability and recovery objectives
4. data classification
5. scaling behavior
6. team operating skill
7. cost model
8. exit and migration strategy

Then justify the service. “It is managed” or “everyone uses it” is not a sufficient architecture decision.

## VPC deep dive (what you must be able to draw)

```text
VPC 10.20.0.0/16
  public-a 10.20.10.0/24  AZ-a   IGW route 0.0.0.0/0
  public-b 10.20.11.0/24  AZ-b
  app-a    10.20.20.0/24  AZ-a   no IGW; optional NAT or endpoints
  app-b    10.20.21.0/24  AZ-b
  data-a   10.20.30.0/24  AZ-a   no NAT; SG only from app SGs
  data-b   10.20.31.0/24  AZ-b
```

Rules of thumb:

- Load balancers of internet-facing type sit in **public** subnets; targets stay **private**
- Databases never get public IPs
- One route table per tier per AZ is easier to reason about than one giant table
- Enable VPC flow logs on a sandbox once so you know what they look like; they cost money in production
- S3/DynamoDB **gateway** endpoints are usually cheaper than NAT for AWS API traffic

IPv4 public addresses now have an hourly cost in AWS. Prefer private + ALB/NLB rather than public EC2.

## Security group patterns

Bad: `0.0.0.0/0` on SSH and RDP.  
Worse: that plus `All traffic`.  
Enterprise: no inbound from internet except the load balancer SG; app SG allows only the LB SG on app port; DB SG allows only the app SG on 5432/3306; egress 443 only unless you have a documented exception.

Reference SGs by **security group ID**, not CIDR, for east-west traffic.

## Compute deep dive

**EC2:** AMIs, instance types, placement, IMDS, user-data vs golden images, SSM, patch manager, ASG lifecycle hooks. Require IMDSv2. No SSH keys in Git. Encrypt EBS with a customer managed key when policy requires it.

**ASG:** desired/min/max, health check type `ELB` vs `EC2`, termination policies, mixed instances, warmup. A rolling deploy that shrinks min to 0 is a self-inflicted outage.

**Lambda:** 15-minute max, payload size, /tmp, VPC ENI cold starts, reserved vs provisioned concurrency, DLQ, idempotency on retries. Lambda in a VPC needs subnet IPs and often endpoints.

**ECS/Fargate:** task definition is the unit of deploy; CPU/memory pairing is fixed for Fargate; execute command is the SSM analogue; task roles vs execution roles (execution pulls images and writes logs).

**EKS/ROSA:** control plane vs data plane, add-ons, IRSA/pod identity, ingress vs OpenShift Route, upgrade skew. EKS is Kubernetes; ROSA is OpenShift on AWS. Pick one platform skill path and be honest about operational cost.

## Storage and data deep dive

**S3 classes:** Standard, IA, Glacier, Intelligent-Tiering. Lifecycle is how you stop log buckets from becoming a second payroll. Object Lock is compliance, not a backup substitute by itself.

**RDS:** parameter groups, option groups, Multi-AZ, read replicas (async), storage autoscaling, Performance Insights, RDS Proxy, snapshot vs PITR. Engine upgrades are change-management events.

**DynamoDB:** partition key cardinality, hot keys, on-demand vs provisioned, GSIs, streams, TTL, PITR, global tables. If you cannot explain the access pattern, do not pick DynamoDB.

## Observability deep dive

| Signal | Tool | Use |
|--------|------|-----|
| Metrics | CloudWatch | saturation, errors, latency |
| Logs | CloudWatch Logs / OpenSearch | debug, audit of app events |
| Traces | X-Ray / OTel | which hop is slow |
| Config | Config | drift |
| API audit | CloudTrail | who changed what |
| Threat | GuardDuty | malware, unusual API |

Golden signals for an HTTP API: availability, latency (p50/p95/p99), traffic, errors (4xx vs 5xx), saturation (CPU, connections, queue).

Alarm design: `5xx rate > 1% for 5 minutes` is better than `CPU > 70%`. CPU is a cause candidate, not a customer symptom.

## Checkpoint

Draw the request path from browser to database including TLS termination, SG hops, and DNS. Then list three ways that path fails and how you would prove each.
