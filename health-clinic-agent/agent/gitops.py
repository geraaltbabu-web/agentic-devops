from __future__ import annotations

import json
from pathlib import Path

from agent.config import state_root
from agent.service import SERVICE


def desired_state_path(environment: str) -> Path:
    return state_root() / "gitops" / "environments" / environment / "desired-state.json"


def read_desired_state(environment: str) -> dict:
    path = desired_state_path(environment)
    return json.loads(path.read_text(encoding="utf-8"))


def write_desired_state(environment: str, image: str, replicas: int) -> dict:
    path = desired_state_path(environment)
    payload = {
        "service": SERVICE,
        "domain": "health",
        "environment": environment,
        "image": image,
        "replicas": replicas,
        "probes": {"path": "/health", "port": 8080},
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


def render_manifest(environment: str, image: str, replicas: int) -> str:
    ns = f"clinic-{environment}"
    return f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {SERVICE}
  namespace: {ns}
  labels:
    app: {SERVICE}
    domain: health
    env: {environment}
spec:
  replicas: {replicas}
  selector:
    matchLabels:
      app: {SERVICE}
  template:
    metadata:
      labels:
        app: {SERVICE}
        domain: health
        env: {environment}
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1001
      containers:
        - name: {SERVICE}
          image: {image}
          ports:
            - containerPort: 8080
              name: http
          readinessProbe:
            httpGet:
              path: /health
              port: http
          resources:
            requests:
              cpu: 50m
              memory: 64Mi
            limits:
              cpu: 200m
              memory: 128Mi
---
apiVersion: v1
kind: Service
metadata:
  name: {SERVICE}
  namespace: {ns}
spec:
  selector:
    app: {SERVICE}
  ports:
    - port: 80
      targetPort: http
"""
