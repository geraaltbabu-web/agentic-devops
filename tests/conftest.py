from __future__ import annotations

import os
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def isolated_state(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("AGENT_STATE_ROOT", str(tmp_path))
    monkeypatch.setenv("AGENT_SIMULATE", "1")
    monkeypatch.delenv("AGENT_LLM_API_KEY", raising=False)
    (tmp_path / "sim").mkdir()
    (tmp_path / "gitops" / "environments" / "dev").mkdir(parents=True)
    yield
