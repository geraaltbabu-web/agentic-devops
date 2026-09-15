# Testing, packaging, safety

## pytest

Test the pure functions (policy, URL builders) without the network. Mock HTTP. CI runs `pytest -q`.

## Safety

- Timeout every network call
- Redact `Authorization`, `token`, `password` in logs (see `health-clinic-agent` redaction)
- `--dry-run` default for anything that mutates
- Do not pickle untrusted data
- Pin base images if you containerize the tool

## Distribution

Wheel + version from Git SHA. Image: non-root USER. Same as later Docker module.
