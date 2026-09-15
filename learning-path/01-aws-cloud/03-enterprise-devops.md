# Enterprise DevOps integration

## Multi-account landing zone

Enterprises separate workloads with AWS Organizations:

- management account: billing and organization only
- security account: GuardDuty/Security Hub administration
- log archive account: immutable organization logs
- shared services account: DNS, directory, networking, tooling
- workload accounts: separate dev, staging, and production boundaries

AWS Control Tower can establish a landing zone. Service control policies set maximum permissions; they do not grant permissions.

## CI/CD authentication with OIDC

GitHub, GitLab, and many CI systems can exchange a signed OIDC token for a short AWS role session:

```text
CI job -> OIDC token -> AWS STS AssumeRoleWithWebIdentity
       -> temporary credentials -> permitted deployment actions
```

Trust policies must constrain repository/project, branch/tag, audience, and environment. The deployment role should be different from the build role. Production should require a protected environment and human approval.

Never store permanent AWS access keys as general CI variables.

## Enterprise delivery path

1. Developer opens a pull request
2. CI runs formatting, tests, SAST, SCA, secret and IaC scans
3. Build creates an immutable artifact
4. Artifact gets an SBOM, vulnerability result, signature, and provenance
5. Deployment plan is reviewed
6. Lower environment deploys automatically
7. Smoke, integration, performance, and policy gates run
8. Production approval is recorded
9. Same artifact is promoted—never rebuilt
10. Progressive rollout verifies health; failure triggers rollback

Typical integrations:

- GitHub/GitLab/Jenkins → OIDC → IAM role
- Docker build → ECR
- Terraform → AWS APIs and remote S3 state with locking
- Argo CD → EKS/ROSA desired state
- External Secrets Operator → Secrets Manager
- Fluent Bit/OpenTelemetry → CloudWatch/OpenSearch
- Prometheus/Grafana → Amazon Managed Service alternatives or self-managed stacks

## Terraform state pattern

Use a separate bootstrap process to create:

- versioned, encrypted S3 state bucket
- state locking mechanism supported by your Terraform version
- narrow CI role
- CloudTrail data events for the state bucket

Separate state by blast radius. Do not use one state file for networking, databases, clusters, and every application. Plans are reviewed artifacts; applies occur only from protected CI.

## Container platform integration

For EKS or ROSA:

- use private worker subnets
- map pods/service accounts to IAM roles
- restrict cluster API reachability
- enforce namespaces/projects and network policies
- define requests, limits, probes, disruption budgets, and autoscaling
- collect audit, application, ingress, and platform logs
- use signed images from approved registries
- upgrade regularly and test version skew

## Deployment strategies

- Rolling: simple and resource-efficient
- Blue/green: fast switch and rollback; costs more
- Canary: small traffic percentage with metric gates
- Feature flag: separates code deployment from feature release

A rollback must include schema compatibility. Expand/contract database changes are safer than destructive one-step migrations.

## Pipeline design exercise

Design a pipeline for a container service with:

- pull-request validation
- OIDC authentication
- ECR immutable tag based on commit SHA
- SBOM and signature
- Terraform plan without apply on pull requests
- dev auto-deployment
- staging integration tests
- production approval and canary
- CloudWatch alarm rollback
- audit evidence retained for one year

For every stage, identify the identity, permissions, input, output, failure behavior, timeout, retry policy, and retained evidence.

## OIDC trust policy (study this until you can write it from memory)

Human-readable rules:

1. Principal is the GitHub/GitLab/Jenkins OIDC provider, not `*`
2. `sts:AssumeRoleWithWebIdentity` only
3. `token.actions.githubusercontent.com:aud` equals `sts.amazonaws.com` (GitHub’s usual audience)
4. `sub` is constrained to `repo:ORG/REPO:environment:prod` or a protected ref
5. Optional: `token.actions.githubusercontent.com:ref` equals `refs/heads/main`

Never trust `repo:ORG/*` for production. Never skip `sub`.

See `labs/oidc-trust-policy.example.json` and `labs/github-actions-oidc.example.yml`. They use placeholders only.

## Artifact flow

```text
git commit SHA
  -> CI build
  -> image: 123456789012.dkr.ecr.region.amazonaws.com/app:git-abc123
  -> scan + SBOM + sign
  -> same digest promoted to staging, then prod
```

`latest` is not a version. Mutable tags cause “it worked in staging” incidents.

ECR: image scanning on push, lifecycle to expire untagged images, KMS encryption, resource policy that only the deploy role can pull in prod.

## Terraform on AWS (preview of module 12)

State in S3 + lock. Plan in PR. Apply from protected environment. Providers pin versions. Modules versioned. Separate states:

- `network`
- `platform` (cluster, IAM, DNS)
- `data`
- `apps/<name>`

Do not put database passwords in `terraform.tfvars` committed to Git. Use Secrets Manager data sources or external secret injection.

## GitOps on AWS (preview of module 16)

Argo CD in EKS/ROSA watches Git. Cluster credentials stay in the cluster. AWS is reached via IRSA for ECR pull, ALB controller, ExternalDNS, External Secrets. Git remains the desired state; AWS APIs are implementation.

If both Jenkins and Argo CD can apply the same manifests, you will drift. Pick one mutator per environment.

## Change management that enterprises actually use

- Standard change: pipeline + automated gates
- Normal change: CAB or platform approval for prod
- Emergency change: break-glass + post-incident ticket
- Every prod apply has a change ID in tags or Git commit trailer

CloudTrail + Git SHA + image digest is the audit triangle. If you cannot join those three, you cannot answer “what shipped?”
