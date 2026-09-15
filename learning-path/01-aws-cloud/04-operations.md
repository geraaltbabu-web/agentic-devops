# Operations, security, reliability, and cost

## Production readiness

Define before deployment:

- service owner and escalation path
- SLI/SLO and alert thresholds
- recovery time and recovery point objectives
- capacity assumptions and quotas
- backups and tested restore procedure
- dependency failure behavior
- deployment and rollback method
- dashboards, logs, traces, and runbooks
- threat model and data classification
- cost estimate and budget owner

## Reliability patterns

- distribute stateless capacity across at least two AZs
- remove single-instance dependencies
- use timeouts, bounded retries with jitter, circuit breakers, and idempotency
- use queues to absorb bursts
- protect downstream systems with concurrency limits
- test instance/AZ/dependency failure
- use cross-Region recovery only when business objectives justify its complexity

## Incident workflow

1. Confirm customer impact and severity
2. Assign incident commander and communication owner
3. Stabilize: rollback, fail over, scale, or disable a feature
4. Preserve logs and timeline evidence
5. Diagnose using recent changes, metrics, traces, logs, and CloudTrail
6. Recover and verify business transactions
7. Write a blameless review with owned preventive actions

## Troubleshooting scenarios

### EC2 instance is unreachable

Check instance state/status checks, route table, public/private addressing, security group, NACL, SSM agent/role, OS firewall, disk space, CPU, and system logs. Prefer Session Manager over opening SSH broadly.

### ALB returns 502/503

Check target health reason, listener/rule, target port, security groups in both directions, application binding address, readiness path, response timeout, and deployment events.

### Application receives AccessDenied

Identify caller and exact action/resource. Evaluate role policy, resource policy, KMS key policy, SCP, permission boundary, session conditions, and Region. Confirm with CloudTrail.

### Lambda is slow or throttled

Inspect duration, init duration, concurrency, downstream latency, memory/CPU allocation, VPC networking, retries, and account quotas. Protect dependencies before raising concurrency.

### RDS connections are exhausted

Inspect application pool sizes, leaked/idle connections, replicas, slow queries, failover events, and scaling. Consider RDS Proxy; do not blindly raise the database maximum.

### Unexpected bill

Use Cost Explorer by service, usage type, Region, and tag. Common causes: NAT data processing, idle load balancers, unattached EBS, snapshots, cross-AZ traffic, public IPv4, logs, OpenSearch, and forgotten databases.

## Security baseline

- SCP guardrails and federated access
- MFA and short sessions for privileged roles
- no public storage or databases
- encryption in transit and at rest
- centralized CloudTrail and Config
- GuardDuty and Security Hub ownership
- Inspector/ECR scanning and patch compliance
- secrets rotation and no credentials in code/logs
- least-privilege security groups and IAM
- tested break-glass access with auditing

## Cost controls

- budgets and anomaly detection
- required ownership/expiry tags
- scheduled shutdown for non-production
- rightsizing from measured utilization
- lifecycle old logs and objects
- Savings Plans only after stable usage exists
- delete unused IPs, volumes, snapshots, load balancers, endpoints, and clusters
- account for data transfer and observability ingestion

## Operational drill

Create a tabletop exercise: deployment doubles latency and increases database connections while one AZ loses capacity. Explain detection, triage, mitigation, rollback, data verification, communication, and preventive changes.
