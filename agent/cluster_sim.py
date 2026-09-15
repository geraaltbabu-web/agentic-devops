from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from agent.config import state_root


DEFAULT_STATE = {
    "environments": {
        "dev": {
            "namespace": "demo-dev",
            "release": {"name": "demo-api", "image": "demo-api:1.0.0", "replicas": 1, "revision": 1},
            "ready": True,
            "history": [{"revision": 1, "image": "demo-api:1.0.0", "replicas": 1}],
        },
        "staging": {
            "namespace": "demo-staging",
            "release": {"name": "demo-api", "image": "demo-api:1.0.0", "replicas": 2, "revision": 1},
            "ready": True,
            "history": [{"revision": 1, "image": "demo-api:1.0.0", "replicas": 2}],
        },
        "prod": {
            "namespace": "demo-prod",
            "release": {"name": "demo-api", "image": "demo-api:1.0.0", "replicas": 3, "revision": 1},
            "ready": True,
            "history": [{"revision": 1, "image": "demo-api:1.0.0", "replicas": 3}],
        },
    }
}


class ClusterSim:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or (state_root() / "sim" / "cluster.json")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.save(DEFAULT_STATE)

    def load(self) -> dict:
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, state: dict) -> None:
        self.path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")

    def inspect(self, environment: str) -> dict:
        env = self._env(environment)
        return deepcopy(env)

    def apply(self, environment: str, image: str, replicas: int) -> dict:
        state = self.load()
        env = state["environments"][environment]
        revision = int(env["release"]["revision"]) + 1
        env["history"].append({"revision": revision, "image": image, "replicas": replicas})
        env["release"] = {
            "name": "demo-api",
            "image": image,
            "replicas": replicas,
            "revision": revision,
        }
        env["ready"] = True
        self.save(state)
        return deepcopy(env["release"])

    def rollback(self, environment: str) -> dict:
        state = self.load()
        env = state["environments"][environment]
        if len(env["history"]) < 2:
            raise RuntimeError("No previous revision to roll back to")
        env["history"].pop()
        previous = env["history"][-1]
        env["release"] = {
            "name": "demo-api",
            "image": previous["image"],
            "replicas": previous["replicas"],
            "revision": previous["revision"],
        }
        env["ready"] = True
        self.save(state)
        return deepcopy(env["release"])

    def health(self, environment: str) -> dict:
        env = self._env(environment)
        return {
            "environment": environment,
            "ready": bool(env.get("ready")),
            "image": env["release"]["image"],
            "replicas": env["release"]["replicas"],
        }

    def _env(self, environment: str) -> dict:
        state = self.load()
        if environment not in state["environments"]:
            raise KeyError(f"Unknown environment: {environment}")
        return state["environments"][environment]
