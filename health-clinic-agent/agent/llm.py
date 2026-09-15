from __future__ import annotations

import json
import urllib.error
import urllib.request

from agent.config import ROOT, Settings
from agent.redaction import redact


def complete_json(goal: str, environment: str, settings: Settings) -> dict | None:
    if not settings.llm_api_key:
        return None
    system = (ROOT / "prompts" / "deploy_system.txt").read_text(encoding="utf-8")
    payload = {
        "model": settings.llm_model,
        "temperature": 0,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": system},
            {
                "role": "user",
                "content": f"Environment: {environment}\nGoal: {goal}\nApply requested: {settings.apply}",
            },
        ],
    }
    req = urllib.request.Request(
        f"{settings.llm_base_url.rstrip('/')}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.llm_api_key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None
    content = body["choices"][0]["message"]["content"]
    try:
        return json.loads(redact(content))
    except json.JSONDecodeError:
        return None
