# Agentic DevOps Demo

A minimal reference project for **agentic DevOps** workflows: containerized app, CI pipeline, Kubernetes manifests, and local automation scripts.

## What's included

| Area | Path | Purpose |
|------|------|---------|
| App | `app/` | Small Python HTTP service with health endpoint |
| Container | `Dockerfile` | Production-style image (non-root user) |
| CI | `.github/workflows/ci.yml` | Build, test, and image build on push |
| K8s | `deploy/k8s/` | Deployment + Service for cluster demos |
| Scripts | `scripts/` | Smoke test and deploy helpers |

## Quick start

```bash
# Local run (Python 3.11+)
cd app && pip install -r requirements.txt && python main.py

# Docker
docker build -t agentic-devops-demo:local .
docker run --rm -p 8080:8080 agentic-devops-demo:local
curl http://localhost:8080/health
```

## Kubernetes (demo)

```bash
kubectl apply -f deploy/k8s/
kubectl port-forward svc/agentic-devops-demo 8080:80
curl http://localhost:8080/health
```

## License

MIT
