from __future__ import annotations

import re

_SECRETISH = re.compile(
    r"(?i)(api[_-]?key|token|password|secret|authorization|bearer)\s*[:=]\s*\S+"
)


def redact(text: str) -> str:
    return _SECRETISH.sub(r"\1=[REDACTED]", text)
