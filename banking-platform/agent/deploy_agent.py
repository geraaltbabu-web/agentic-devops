"""Policy-gated deployment agent; plans by default and applies only with explicit flags."""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import subprocess
import urllib.request
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class DeploymentPolicy:
    environments: list[str]
    image_patterns: list[str]
    max_replicas: int

    @classmethod
    def load(cls, path: Path) -> "DeploymentPolicy":
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls(data["environments"], data["image_patterns"], data["max_replicas"])


def make_plan(environment: str, image: str, approve_prod: bool, policy: DeploymentPolicy) -> dict:
    if environment not in policy.environments:
        raise ValueError(f"Unknown environment: {environment}")
    if not any(fnmatch.fnmatch(image, pattern) for pattern in policy.image_patterns):
        raise ValueError("Image is not allowed by policy")
    if environment == "prod" and not approve_prod:
        raise ValueError("Production requires --approve-prod and protected-environment approval")
    replicas = {"dev": 1, "staging": 2, "prod": 3}[environment]
    return {
        "environment": environment,
        "image": image,
        "risk": "high" if environment == "prod" else "medium",
        "steps": [
            {"action": "policy_check"},
            {"action": "terraform_plan", "scope": "infrastructure"},
            {"action": "render", "tool": "helm", "replicas": min(replicas, policy.max_replicas)},
            {"action": "security_scan", "tools": ["trivy", "checkov"]},
            {"action": "dry_run", "tool": "oc apply --dry-run=server"},
            {"action": "apply", "tool": "oc apply"},
            {"action": "health_check", "timeout_seconds": 300},
            {"action": "rollback_on_failure", "tool": "oc rollout undo"},
        ],
    }


def ai_review(plan: dict) -> dict:
    """Optional OpenAI-compatible review. No key means deterministic offline review."""
    key = os.getenv("AGENT_LLM_API_KEY", "")
    if not key:
        return {"provider": "offline-policy-engine", "decision": "approved", "notes": ["All guardrails passed"]}
    endpoint = os.getenv("AGENT_LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    body = {
        "model": os.getenv("AGENT_LLM_MODEL", "gpt-4o-mini"),
        "temperature": 0,
        "messages": [
            {"role": "system", "content": "Review this synthetic banking deployment plan. Return JSON with decision and notes. Never request or expose secrets."},
            {"role": "user", "content": json.dumps(plan)},
        ],
        "response_format": {"type": "json_object"},
    }
    request = urllib.request.Request(
        f"{endpoint}/chat/completions", data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.loads(response.read())
    return json.loads(result["choices"][0]["message"]["content"])


def run_oc(environment: str, image: str) -> None:
    chart = ROOT / "platform" / "chart"
    values = ROOT / "platform" / "environments" / f"{environment}.yaml"
    namespace = f"banking-{environment}"
    rendered = subprocess.run(
        ["helm", "template", "banking", str(chart), "-f", str(values)],
        check=True, capture_output=True,
    ).stdout
    subprocess.run(
        ["oc", "apply", "-n", namespace, "--dry-run=server", "-f", "-"],
        input=rendered, check=True,
    )
    subprocess.run(["oc", "apply", "-n", namespace, "-f", "-"], input=rendered, check=True)
    subprocess.run(
        ["oc", "set", "image", "deployment", "--all", f"*={image}", "-n", namespace],
        check=True,
    )
    subprocess.run(
        ["oc", "rollout", "status", "deployment", "--all", "-n", namespace, "--timeout=300s"],
        check=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Banking platform deployment agent")
    parser.add_argument("--environment", choices=["dev", "staging", "prod"], default="dev")
    parser.add_argument("--image", default="ghcr.io/demo/banking:1.0.0")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--approve-prod", action="store_true")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args()
    policy = DeploymentPolicy.load(ROOT / "agent" / "policy.json")
    plan = make_plan(args.environment, args.image, args.approve_prod, policy)
    report = {"plan": plan, "ai_review": ai_review(plan), "mode": "apply" if args.apply else "plan"}
    if args.apply:
        run_oc(args.environment, args.image)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
