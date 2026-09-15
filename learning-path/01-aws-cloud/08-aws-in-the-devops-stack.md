# How AWS shows up in the rest of the DevOps stack

Every later module plugs into AWS. Learn the **interface**, not vendor trivia.

## Linux (next module)

EC2 and container hosts are Linux. You will use systemd, journald, disks, ulimits, and networking on AMIs and node images. SSM Session Manager is SSH with IAM. If you cannot read a unit file, you cannot debug an instance that “is running but the app is down.”

## GitHub / GitLab / Jenkins

Git is the system of record. CI is a **principal** in IAM via OIDC. Jenkins needs the same trust constraints as GitHub Actions: exact repo/job, short session, separate plan vs apply roles. Groovy/Jenkinsfiles must not print `AWS_SECRET_ACCESS_KEY`.

## Docker and ECR

Build on CI, push digest to ECR, pull from private subnets via endpoint. Image scan is not a substitute for a patched base. `latest` is forbidden in prod.

## Kubernetes / OpenShift (OCP) / ROSA

The cluster runs in private subnets. IRSA or OpenShift cloud credential operator maps workloads to IAM. Ingress/Routes terminate TLS. Cluster autoscaler talks to EC2. The control plane is AWS’s (EKS/ROSA) or yours (self-managed—avoid in this course).

## Terraform

Terraform calls the same APIs as the CLI. State in S3. Locks. CI role can `plan` broadly and `apply` narrowly. Providers pin versions.

## Argo CD

Argo CD does not replace AWS. It applies Kubernetes objects that then create AWS resources through controllers (ALB, ExternalDNS). Protect the Git repo; protect the cluster RBAC; protect the IAM roles the controllers use.

## Databases

RDS/Aurora still need SG, subnet groups, parameter groups, backups, and pipeline-safe migrations. Connection strings live in Secrets Manager, not Helm values committed to Git.

## ELK / OpenSearch

Self-managed ELK on EC2/EKS costs operations. OpenSearch Service costs money quickly. In sandbox, prefer CloudWatch Logs. In enterprises, logs go to a **log archive account** with retention and legal hold.

## Prometheus and Grafana

You can use Amazon Managed Prometheus/Grafana or run them on the cluster. Metrics cardinality can cost as much as compute. Alertmanager routes still need on-call ownership.

## Ansible / Vault / security scanners

Ansible uses SSM or SSH via IAM-controlled access. Vault or Secrets Manager holds secrets; AWS KMS wraps keys. SAST/SCA/IaC scans run in CI before any AWS apply.

## Mental model to keep

```text
Git (desired)
  -> CI (OIDC identity)
    -> Artifact (ECR digest)
    -> Infra API (CloudFormation/Terraform)
    -> Runtime (EC2/ECS/EKS/ROSA)
      -> Data (RDS/S3)
      -> Signals (CloudWatch/ELK/Prom)
```

If you cannot point to the identity at each arrow, you do not yet own the design.
