from __future__ import annotations

import argparse
import json
import sys

from agent.config import Settings
from agent.executor import Executor, execute_plan
from agent.planner import build_plan
from agent.policies import PolicyViolation, assert_goal_safe, load_policies
from agent.redaction import redact


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generic AI deployment agent")
    parser.add_argument("command", choices=["plan", "deploy", "review", "rollback"])
    parser.add_argument("--goal", default="")
    parser.add_argument("--env", default="")
    parser.add_argument("--image", default="demo-api:1.1.0")
    parser.add_argument("--replicas", type=int, default=1)
    parser.add_argument("--apply", action="store_true", help="Execute mutating steps")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def goal_for(command: str, args: argparse.Namespace, environment: str) -> str:
    if args.goal:
        return args.goal
    if command == "review":
        return f"review manifests for {environment}"
    if command == "rollback":
        return f"rollback {environment}"
    if command == "plan":
        return f"plan rollout of {args.image} to {environment}"
    return f"deploy {args.image} to {environment} with {args.replicas} replicas"


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    settings = Settings.from_env()
    environment = args.env or settings.default_env
    apply = False if args.command in {"plan", "review"} else (args.apply or settings.apply)
    if args.command == "rollback":
        apply = args.apply or settings.apply
    goal = goal_for(args.command, args, environment)

    try:
        assert_goal_safe(goal, load_policies())
        effective = Settings(
            llm_base_url=settings.llm_base_url,
            llm_model=settings.llm_model,
            llm_api_key=settings.llm_api_key,
            apply=apply,
            approve_prod=settings.approve_prod,
            simulate=settings.simulate,
            default_env=settings.default_env,
        )
        plan = build_plan(goal, environment, args.image, args.replicas, effective)
        executor = Executor(
            simulate=settings.simulate,
            apply=apply,
            approve_prod=settings.approve_prod,
        )
        outcome = execute_plan(plan, executor)
    except PolicyViolation as exc:
        print(redact(str(exc)), file=sys.stderr)
        return 2

    report = {"goal": goal, "environment": environment, "plan": plan, "outcome": outcome}
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Goal: {goal}")
        print(f"Env:  {environment}")
        print(f"Plan: {plan['summary']} (risk={plan['risk']})")
        for step in plan["steps"]:
            print(f"  - {step['tool']} {step.get('args', {})}")
        print(f"Result: {outcome['status']}")
        if outcome["status"] != "ok":
            last = outcome["results"][-1]
            print(f"Failed at {last.get('tool')}: {last.get('error') or last.get('result')}")
            return 1
    return 0 if outcome["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
