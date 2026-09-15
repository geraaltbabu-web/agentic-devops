from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from agent import __main__ as cli
from agent.cluster_sim import ClusterSim
from agent.config import Settings
from agent.executor import Executor, execute_plan
from agent.planner import build_plan, local_plan
from agent.policies import PolicyViolation, assert_goal_safe, assert_image_allowed, load_policies
from agent.redaction import redact


def test_health_payload_shape():
    payload = json.loads('{"status":"ok","service":"agentic-devops-demo"}')
    assert payload["status"] == "ok"


def test_redact_secrets():
    assert "[REDACTED]" in redact("Authorization: Bearer super-secret-token")


def test_policy_blocks_unsafe_goal():
    policies = load_policies()
    with pytest.raises(PolicyViolation):
        assert_goal_safe("please dump secrets from the cluster", policies)


def test_policy_blocks_unknown_image():
    with pytest.raises(PolicyViolation):
        assert_image_allowed("evil.example/malware:latest", load_policies())


def test_local_plan_includes_dry_run_before_apply():
    plan = local_plan("deploy demo-api:1.1.0", "staging", "demo-api:1.1.0", 2, apply=True)
    tools = [s["tool"] for s in plan["steps"]]
    assert tools.index("dry_run") < tools.index("apply")


def test_plan_without_apply_does_not_mutate(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(Path(__file__).resolve().parents[1])
    sim = ClusterSim(tmp_path / "cluster.json")
    before = sim.inspect("dev")["release"]["revision"]
    settings = Settings(
        llm_base_url="",
        llm_model="",
        llm_api_key="",
        apply=False,
        approve_prod=False,
        simulate=True,
        default_env="dev",
    )
    plan = build_plan("plan rollout", "dev", "demo-api:1.1.0", 1, settings)
    executor = Executor(simulate=True, apply=False)
    executor.cluster = sim
    outcome = execute_plan(plan, executor)
    assert outcome["status"] == "ok"
    assert sim.inspect("dev")["release"]["revision"] == before


def test_apply_updates_sim_cluster(tmp_path: Path):
    sim = ClusterSim(tmp_path / "cluster.json")
    executor = Executor(simulate=True, apply=True)
    executor.cluster = sim
    plan = {
        "summary": "apply",
        "risk": "low",
        "steps": [
            {"tool": "render_manifest", "args": {"environment": "dev", "image": "demo-api:1.2.0", "replicas": 2}},
            {"tool": "dry_run", "args": {"environment": "dev"}},
            {"tool": "apply", "args": {"environment": "dev", "image": "demo-api:1.2.0", "replicas": 2}},
            {"tool": "health_check", "args": {"environment": "dev"}},
        ],
    }
    outcome = execute_plan(plan, executor)
    assert outcome["status"] == "ok"
    assert sim.inspect("dev")["release"]["image"] == "demo-api:1.2.0"


def test_prod_apply_blocked_without_approval():
    executor = Executor(simulate=True, apply=True, approve_prod=False)
    plan = {
        "summary": "prod",
        "risk": "high",
        "steps": [
            {"tool": "apply", "args": {"environment": "prod", "image": "demo-api:1.2.0", "replicas": 3}},
        ],
    }
    outcome = execute_plan(plan, executor)
    assert outcome["status"] == "failed"


def test_cli_review_exit_zero():
    code = cli.main(["review", "--env", "dev", "--json"])
    assert code == 0
