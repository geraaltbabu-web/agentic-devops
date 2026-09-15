# Agentic DevOps

Generic, company-agnostic **end-to-end DevOps agent** demo. An AI planner proposes a deployment, guardrails validate it, GitOps desired state is updated, then a simulated cluster is dry-run / applied / health-checked.

This repository contains **no customer, product, or internal-company data**. Sample names are `demo-api`, `dev`, `staging`, and `prod`.

## Flow

```
goal --> planner (LLM or local) --> policy gates --> GitOps update
      --> kubectl-style dry-run --> apply (optional) --> health check --> report
```

| Layer | Path | Role |
|-------|------|------|
| Sample app | `app/` | Tiny HTTP service with `/health` |
| Agent | `agent/` | Plan, review, deploy, rollback CLI |
| Guardrails | `policies/guardrails.json` | Image allowlist, prod lock, secret redaction |
| GitOps | `gitops/environments/` | Desired state per environment |
| Simulator | `sim/cluster.json` | In-process cluster so CI needs no kubeconfig |
| Helm | `deploy/helm/demo-api/` | Optional chart for real clusters |
| CI | `.github/workflows/` | Test, agent review, manual agent deploy |

## Quick start

```bash
# from repo root
export PYTHONPATH=.
python -m agent plan --env staging --image demo-api:1.1.0
python -m agent review --env staging
python -m agent deploy --env staging --image demo-api:1.1.0          # plan + dry-run
python -m agent deploy --env staging --image demo-api:1.1.0 --apply  # mutates simulator
```

Production apply is blocked unless `APPROVE_PROD=true` **and** `--apply` is set.

## Optional LLM

If `AGENT_LLM_API_KEY` is set, the planner calls an OpenAI-compatible `/chat/completions` endpoint. If it is unset or the call fails, a deterministic local planner is used. See `.env.example`.

Store keys only in GitHub Actions secrets or a local `.env` (never commit them).

## Docker

```bash
docker compose up --build demo-api
curl http://localhost:8080/health

docker compose run --rm agent plan --env dev --image demo-api:1.1.0 --json
```

## Tests

```bash
pip install pytest
PYTHONPATH=. pytest -q
```

## GitHub Actions

- **CI** — unit tests, agent plan, image builds
- **Agent review** — PR review of deploy/GitOps changes
- **Agent deploy** — `workflow_dispatch` with environment, image, apply, and prod approval flags

For a real cluster later, keep `AGENT_SIMULATE=1` until you replace `ClusterSim` with `kubectl` behind the same tool interface. Do not point this demo at production systems that hold private data.

## License

MIT
