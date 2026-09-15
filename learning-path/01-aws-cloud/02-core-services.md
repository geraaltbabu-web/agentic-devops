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
