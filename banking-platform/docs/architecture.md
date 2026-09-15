# Architecture

```mermaid
flowchart LR
  U[Client] --> R[OpenShift Routes / TLS]
  R --> A[Accounts]
  R --> P[Payments]
  R --> L[Ledger]
  R --> F[Fraud]
  R --> N[Notifications]
  P --> A
  P --> F
  P --> L
  P --> N
  A & P & L & F & N --> LS[Log collector]
  LS --> OS[AWS OpenSearch / local ELK]
  OS --> K[Kibana / Dashboards]
```

```mermaid
flowchart TD
  C[Git commit] --> CI[Tests + secret scan + Helm/Terraform validation]
  CI --> I[Immutable container image]
  I --> D[Deployment-agent plan]
  D --> G{Policy gates}
  G -->|reject| X[Stop and report]
  G -->|approve| DR[OpenShift server dry-run]
  DR --> AP[Apply / Argo CD sync]
  AP --> H[Readiness + rollout verification]
  H -->|failure| RB[Automatic rollback]
  H -->|healthy| O[ELK/OpenSearch observability]
```

## Design boundaries

- All data is synthetic. The sample is not suitable for processing real financial information.
- Services run independently and communicate through HTTP in the demo.
- Local mode uses Docker Compose and optional ELK.
- Cloud mode uses AWS infrastructure, ROSA (managed OpenShift), Helm, and OpenShift GitOps.
- The AI reviews a bounded JSON plan; deterministic policy remains authoritative.
- Production uses a GitHub protected environment, explicit approval, immutable images, dry-run, rollout checks, and rollback.
