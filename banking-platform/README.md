# Agentic banking platform

A runnable, synthetic banking microservices project with AI-assisted deployment, AWS infrastructure, ROSA/OpenShift, GitOps, and ELK/OpenSearch. It contains no real customer or financial data.

## What you get

- Five services: accounts, payments, ledger, fraud, notifications
- NGINX local API gateway and structured correlation IDs
- Docker Compose local deployment; optional Elasticsearch, Logstash, Kibana
- Terraform for AWS VPC, ECR, KMS, audit S3, OpenSearch, and ROSA Hosted Control Plane
- Helm chart for OpenShift with Routes, TLS, probes, resources, HPA, and network policies
- Argo CD/OpenShift GitOps application
- Policy-gated AI deployment planner with plan-only default, production approval, dry-run, health verification, and rollback intent
- GitHub Actions validation and manually approved deployment

See [the architecture diagrams](docs/architecture.md).

## Path A — run locally (recommended first)

Prerequisites: Git, Docker Desktop with Compose, and Python 3.12+.

```powershell
cd banking-platform
.\scripts\verify.ps1
docker compose up --build -d
curl http://localhost:8080/health
curl http://localhost:8080/api/accounts
```

Test a synthetic payment:

```powershell
curl -Method POST http://localhost:8080/api/payments `
  -ContentType application/json `
  -Body '{"amount":125.50,"currency":"USD","destination":"acct-demo-002"}'
```

Stop everything:

```powershell
docker compose down
```

### Add local ELK

ELK needs roughly 2 GB free memory:

```powershell
docker compose --profile observability up --build -d
curl http://localhost:9200
Start-Process http://localhost:5601
```

Kibana opens at `http://localhost:5601`. Create an index pattern `banking-services-*` after sending logs to Logstash.

## Path B — inspect the deployment agent

Safe plan only; this needs no cloud account:

```powershell
python agent/deploy_agent.py `
  --environment staging `
  --image ghcr.io/demo/banking:1.0.0
```

Set `AGENT_LLM_API_KEY` (and optionally `AGENT_LLM_BASE_URL`, `AGENT_LLM_MODEL`) to add an OpenAI-compatible review. Without a key, the offline policy engine is used. AI cannot bypass policy.

## Path C — deploy AWS + OpenShift

This path creates chargeable resources. ROSA also requires an enabled AWS account, Red Hat organization access, service quotas, and an OpenShift Cluster Manager token.

Prerequisites:

1. AWS CLI authenticated to a sandbox account
2. Terraform 1.7+
3. ROSA CLI, `oc`, and Helm 3
4. ROSA CLI logged in with an OpenShift Cluster Manager offline token

```powershell
cd infra\terraform
rosa login --token="<your-red-hat-offline-token>"
terraform init
terraform fmt -check
terraform validate
terraform plan -var="environment=dev" -out=dev.tfplan
terraform apply dev.tfplan
terraform output
```

Then authenticate to the new cluster and install the workload:

```powershell
oc login <cluster-api-url> --token=<token>
oc new-project banking-dev
helm upgrade --install banking .\platform\chart `
  -f .\platform\environments\dev.yaml `
  -n banking-dev
oc get pods,route -n banking-dev
```

For GitOps, install OpenShift GitOps and apply:

```powershell
oc apply -f gitops\argocd-application.yaml
oc get application -n openshift-gitops banking-platform
```

## GitHub setup

1. Add protected environments: `dev`, `staging`, `prod`; require reviewers for `prod`.
2. Add environment secrets `OPENSHIFT_SERVER` and `OPENSHIFT_TOKEN`.
3. Optionally add `AGENT_LLM_API_KEY`; add variables `AGENT_LLM_BASE_URL` and `AGENT_LLM_MODEL`.
4. Open **Actions → Banking agent deploy → Run workflow**.
5. Keep `apply=false` for a plan. Set it true only after reviewing the plan.

## Important limitations

This is a detailed reference implementation, not a certified banking product. Before real use, add an identity provider, mTLS/service mesh, real databases with migration and backup, PCI DSS controls, WAF, SIEM rules, disaster recovery, load tests, signed images, SBOM attestations, and organization-specific threat modeling.

Destroy sandbox infrastructure when finished:

```powershell
terraform -chdir=infra/terraform destroy -var="environment=dev"
```
