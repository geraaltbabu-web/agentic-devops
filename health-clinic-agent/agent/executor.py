from __future__ import annotations

from agent.cluster_sim import ClusterSim
from agent.gitops import render_manifest, write_desired_state
from agent.policies import (
    PolicyViolation,
    assert_apply_allowed,
    assert_image_allowed,
    assert_replicas,
    load_policies,
)
from agent.redaction import redact


class Executor:
    def __init__(self, simulate: bool = True, apply: bool = False, approve_prod: bool = False) -> None:
        self.simulate = simulate
        self.apply = apply
        self.approve_prod = approve_prod
        self.policies = load_policies()
        self.cluster = ClusterSim()
        self.last_manifest = ""

    def run_step(self, tool: str, args: dict) -> dict:
        environment = args.get("environment", "dev")
        if tool == "inspect_cluster":
            return {"ok": True, "cluster": self.cluster.inspect(environment)}
        if tool == "update_gitops":
            image = args["image"]
            replicas = int(args.get("replicas", 1))
            assert_image_allowed(image, self.policies)
            assert_replicas(replicas, self.policies)
            state = write_desired_state(environment, image, replicas)
            return {"ok": True, "desired_state": state}
        if tool == "render_manifest":
            image = args["image"]
            replicas = int(args.get("replicas", 1))
            assert_image_allowed(image, self.policies)
            assert_replicas(replicas, self.policies)
            self.last_manifest = render_manifest(environment, image, replicas)
            return {"ok": True, "manifest": self.last_manifest}
        if tool == "dry_run":
            if not self.last_manifest:
                image = args.get("image", "clinic-api:1.0.0")
                replicas = int(args.get("replicas", 1))
                self.last_manifest = render_manifest(environment, image, replicas)
            return {
                "ok": True,
                "mode": "client-dry-run",
                "simulated": self.simulate,
                "bytes": len(self.last_manifest.encode("utf-8")),
            }
        if tool == "apply":
            assert_apply_allowed(environment, True, self.approve_prod, self.policies)
            if not self.apply:
                raise PolicyViolation("Apply blocked: set AGENT_APPLY=true to execute")
            image = args.get("image") or self.cluster.inspect(environment)["release"]["image"]
            replicas = int(args.get("replicas") or self.cluster.inspect(environment)["release"]["replicas"])
            assert_image_allowed(image, self.policies)
            assert_replicas(replicas, self.policies)
            release = self.cluster.apply(environment, image, replicas)
            return {"ok": True, "applied": release, "simulated": self.simulate}
        if tool == "health_check":
            health = self.cluster.health(environment)
            if not health["ready"]:
                return {"ok": False, "health": health}
            return {"ok": True, "health": health}
        if tool == "rollback":
            assert_apply_allowed(environment, True, self.approve_prod, self.policies)
            if not self.apply:
                raise PolicyViolation("Rollback blocked: set AGENT_APPLY=true to execute")
            release = self.cluster.rollback(environment)
            return {"ok": True, "rolled_back_to": release}
        raise PolicyViolation(f"Unknown tool: {tool}")


def execute_plan(plan: dict, executor: Executor) -> dict:
    results = []
    for step in plan.get("steps", []):
        tool = step["tool"]
        args = step.get("args") or {}
        try:
            result = executor.run_step(tool, args)
            results.append({"tool": tool, "ok": True, "result": result})
            if not result.get("ok", True):
                return {"status": "failed", "results": results}
        except Exception as exc:  # noqa: BLE001 - surface policy and runtime errors
            results.append({"tool": tool, "ok": False, "error": redact(str(exc))})
            return {"status": "failed", "results": results}
    return {"status": "ok", "results": results}
