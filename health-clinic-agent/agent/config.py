from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def state_root() -> Path:
    override = os.environ.get("AGENT_STATE_ROOT")
    return Path(override) if override else ROOT


@dataclass(frozen=True)
class Settings:
    llm_base_url: str
    llm_model: str
    llm_api_key: str
    apply: bool
    approve_prod: bool
    simulate: bool
    default_env: str

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            llm_base_url=os.environ.get("AGENT_LLM_BASE_URL", "https://api.openai.com/v1"),
            llm_model=os.environ.get("AGENT_LLM_MODEL", "gpt-4o-mini"),
            llm_api_key=os.environ.get("AGENT_LLM_API_KEY", ""),
            apply=os.environ.get("AGENT_APPLY", "false").lower() in {"1", "true", "yes"},
            approve_prod=os.environ.get("APPROVE_PROD", "false").lower() in {"1", "true", "yes"},
            simulate=os.environ.get("AGENT_SIMULATE", "1").lower() not in {"0", "false", "no"},
            default_env=os.environ.get("AGENT_ENV", "dev"),
        )
