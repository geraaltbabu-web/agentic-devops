from __future__ import annotations

import fnmatch
import json
from dataclasses import dataclass
from pathlib import Path

from agent.config import ROOT


@dataclass
class PolicyViolation(Exception):
    message: str

    def __str__(self) -> str:
        return self.message


def load_policies(path: Path | None = None) -> dict:
    policy_path = path or (ROOT / "policies" / "guardrails.json")
    return json.loads(policy_path.read_text(encoding="utf-8"))


def assert_goal_safe(goal: str, policies: dict) -> None:
    lowered = goal.lower()
    for pattern in policies.get("blocked_goal_patterns", []):
        if pattern.lower() in lowered:
            raise PolicyViolation(f"Goal blocked by guardrail: {pattern}")


def assert_image_allowed(image: str, policies: dict) -> None:
    for pattern in policies.get("image_allowlist", []):
        if fnmatch.fnmatch(image, pattern):
            return
    raise PolicyViolation(f"Image not on allowlist: {image}")


def assert_replicas(replicas: int, policies: dict) -> None:
    max_replicas = int(policies.get("max_replicas", 10))
    if replicas < 1 or replicas > max_replicas:
        raise PolicyViolation(f"Replica count {replicas} outside 1..{max_replicas}")


def assert_apply_allowed(environment: str, apply: bool, approve_prod: bool, policies: dict) -> None:
    if not apply:
        return
    forbidden = {e.lower() for e in policies.get("forbidden_apply_environments", [])}
    if environment.lower() in forbidden and not approve_prod:
        raise PolicyViolation(
            f"Apply to {environment} is forbidden without APPROVE_PROD=true"
        )
