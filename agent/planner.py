from __future__ import annotations

from agent.config import Settings
from agent.llm import complete_json


def local_plan(goal: str, environment: str, image: str, replicas: int, apply: bool) -> dict:
    lowered = goal.lower()
    if "rollback" in lowered:
        steps = [
            {"tool": "inspect_cluster", "args": {"environment": environment}},
            {"tool": "rollback", "args": {"environment": environment}},
            {"tool": "health_check", "args": {"environment": environment}},
        ]
        return {"summary": f"Rollback {environment}", "risk": "medium", "steps": steps}

    if "review" in lowered or "audit" in lowered:
        steps = [
            {"tool": "inspect_cluster", "args": {"environment": environment}},
            {"tool": "render_manifest", "args": {"environment": environment, "image": image, "replicas": replicas}},
            {"tool": "dry_run", "args": {"environment": environment}},
        ]
        return {"summary": f"Review desired state for {environment}", "risk": "low", "steps": steps}

    steps = [
        {"tool": "inspect_cluster", "args": {"environment": environment}},
        {
            "tool": "update_gitops",
            "args": {"environment": environment, "image": image, "replicas": replicas},
        },
        {
            "tool": "render_manifest",
            "args": {"environment": environment, "image": image, "replicas": replicas},
        },
        {"tool": "dry_run", "args": {"environment": environment}},
    ]
    if apply:
        steps.append({"tool": "apply", "args": {"environment": environment, "image": image, "replicas": replicas}})
        steps.append({"tool": "health_check", "args": {"environment": environment}})
    return {
        "summary": f"{'Apply' if apply else 'Plan'} {image} to {environment}",
        "risk": "high" if environment == "prod" else "low",
        "steps": steps,
    }


def build_plan(
    goal: str,
    environment: str,
    image: str,
    replicas: int,
    settings: Settings,
) -> dict:
    llm_plan = complete_json(goal, environment, settings)
    if isinstance(llm_plan, dict) and isinstance(llm_plan.get("steps"), list):
        llm_plan.setdefault("summary", goal)
        llm_plan.setdefault("risk", "medium")
        return llm_plan
    return local_plan(goal, environment, image, replicas, settings.apply)
