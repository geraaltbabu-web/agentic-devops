# HTTP, CLI, and files

## CLI

`argparse` with subcommands: `plan` vs `apply`. Exit codes: 0 ok, 1 operational fail, 2 usage. JSON `--json` for other tools to consume.

## HTTP

stdlib `urllib` is enough for labs. Production: timeouts, retries with jitter, idempotency keys, User-Agent, correlation ID header. Never disable TLS verify except a documented lab.

## Files and subprocess

- Read configs as JSON/YAML; validate required keys
- `subprocess.run(..., check=True, capture_output=True, text=True)` — do not `shell=True` with user input
- Env vars for secrets, not argv (`ps` sees argv)

## AWS / K8s clients (preview)

boto3: sessions + paginators (see AWS inventory lab). Kubernetes: in-cluster service account vs kubeconfig. Same IAM lesson: the process identity matters more than the library.
