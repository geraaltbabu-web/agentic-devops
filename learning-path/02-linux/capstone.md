# Capstone — node that could run a service

Design and demonstrate (on WSL/VM, not a work production host):

1. A non-root user and a directory tree for an app (`/opt` or `/srv` style under a temp prefix is fine on WSL)
2. A tiny HTTP process (Python from Lab 3 is enough) bound to `127.0.0.1`
3. A health check script from Lab 5 wired to that port
4. A one-page runbook: disk full, port not listening, DNS fail, permission denied
5. How this maps to an EC2 instance behind an ALB (bind `0.0.0.0` vs localhost; SG; systemd unit sketch)

## Deliverables

- Diagram: user → systemd/process → socket → curl
- Unit file *sketch* (`User=`, `ExecStart=`, `Restart=on-failure`) even if you cannot install it on WSL
- Sanitized command transcript (no `/etc/shadow`, no keys)
- Three injected failures and how you proved each

## Pass bar

Another engineer can follow your notes on a clean Ubuntu VM, bring the process up, break it, and fix it without `chmod 777`.
