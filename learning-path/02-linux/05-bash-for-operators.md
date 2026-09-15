# Bash for operators

## Non-negotiable header

```bash
#!/usr/bin/env bash
set -euo pipefail
```

| Option | Why |
|--------|-----|
| `-e` | Fail on error |
| `-u` | Fail on unset variables |
| `-o pipefail` | Fail if any pipe stage fails |

Exceptions: you *want* a command to fail (use `|| true` with a comment).

## Quoting

Always quote `"$var"`. Unquoted `$files` is how you delete the wrong things. Use arrays, not string splitting, for lists.

`$@` vs `$*`. Prefer `"$@"`.

## Tests and files

```bash
[[ -d "$dir" ]] || { echo "missing $dir" >&2; exit 1; }
[[ -n "${NAME:-}" ]] || exit 2
```

`[` vs `[[`: use `[[` in Bash.

## Output and logs

- Logs to stderr: `echo "..." >&2`
- Machine output to stdout (so `| jq` works)
- `logger -t myscript` for syslog/journal
- Never `echo $PASSWORD`

## Idempotence

A check script can run twice. `mkdir -p`. `grep -q &&` before appending to a file. Do not append forever.

## Cron vs systemd timers vs CI

Cron has a minimal environment (`PATH` is short). Always set `PATH` or use absolute paths. Prefer systemd timers on servers you own.

## Linting

`shellcheck` on every script you would run as root. Treat warnings as defects.

## What not to automate in Bash

- Complex JSON/YAML (use Python/`jq`)
- Parallel fleet changes (use Ansible)
- Anything with secrets in argv (`ps` sees argv)

## Checkpoint

Write a 20-line script that: checks a URL, checks disk `%` on `/`, prints JSON, exits non-zero on fail, and is `shellcheck`-clean.
