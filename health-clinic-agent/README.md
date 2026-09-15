# Agentic DevOps — health (clinic) demo

This is a **synthetic clinic** sample: appointments and health checks only. It is **not** banking or telecom, and it is **not** a real hospital system (no PHI, no patient names, no medical records).

## Will it run if I follow the steps?

**Yes for the demo path** (Python app + AI agent against a **simulated** cluster). That is what the steps below do.

| Path | Runs by following steps? | Notes |
|------|--------------------------|--------|
| Unit tests + agent plan/apply on simulator | Yes | Needs Python 3.12+ |
| Clinic API on localhost | Yes | `python app/main.py` or Docker |
| GitHub Actions CI | Yes on GitHub-hosted runners | After the latest push |
| Optional LLM planner | Only if you add an API key | Without a key, local planner is used |
| Real Kubernetes/Helm apply | No by default | Manifests exist; you need a cluster |

Production **apply** stays blocked unless you set `APPROVE_PROD=true`.

## 1) Verify (one script)

```powershell
cd c:\Users\vishbhag\git\agentic-devops\health-clinic-agent
.\scripts\verify.ps1
```

Expected: tests pass, then an agent **plan** for `clinic-api` on `staging` ends with `Result: ok`.

## 2) Run the clinic API

```powershell
python app\main.py
```

In another terminal:

```powershell
curl http://localhost:8080/health
curl http://localhost:8080/appointments
```

Or Docker:

```powershell
docker compose up --build clinic-api
```

## 3) Let the agent deploy (simulator)

```powershell
.\scripts\run-agent.ps1 -Command plan -Environment staging -Image clinic-api:1.1.0
.\scripts\run-agent.ps1 -Command deploy -Environment staging -Image clinic-api:1.1.0 -Apply
```

`--apply` updates `sim/cluster.json` only. It does not touch a real cluster.

## Layout

| Path | Role |
|------|------|
| `app/` | Clinic API (`/health`, `/appointments`) |
| `agent/` | Plan / review / deploy / rollback |
| `policies/` | Guardrails |
| `gitops/environments/` | Desired state |
| `sim/` | Fake cluster |
| `deploy/helm/clinic-api/` | Optional Helm chart |

## License

MIT
