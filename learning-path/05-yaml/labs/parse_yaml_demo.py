"""Optional: pip install pyyaml. Shows bool vs string footguns."""
from __future__ import annotations

try:
    import yaml
except ImportError:
    print("Install pyyaml to run this lab, or just read app.yaml comments.")
    raise SystemExit(0)

unsafe = yaml.safe_load("on: no\n")
safe = yaml.safe_load('on: "no"\n')
print("unquoted:", unsafe)
print("quoted:", safe)
