# Processes, systemd, and logs

## Processes

```text
ps aux
ps -ef
top / htop
pgrep -a nginx
pstree -p
```

Each process has: PID, PPID, UID, cwd (`ls -l /proc/PID/cwd`), open files (`ls -l /proc/PID/fd`), environment (`/proc/PID/environ` — may contain secrets; do not dump to Git).

Signals you must know:

| Signal | Typical use |
|--------|-------------|
| TERM (15) | Please stop |
| KILL (9) | Kernel stops it; no cleanup |
| HUP (1) | Reload config (many daemons) |
| INT (2) | Ctrl-C |

Prefer TERM and a systemd timeout over KILL. KILL leaves sockets and children.

Nice/renice: CPU niceness, not I/O. `ionice` exists. Production is cgroups (systemd slices, containers).

OOM killer: host kills a process when memory is exhausted. `dmesg` / journal `oom`. The fix is limits, leaks, or more memory—not silence.

## systemd

systemd is the PID 1 on modern servers (WSL2 Ubuntu may use systemd depending on version/config).

Core objects:

- **unit:** `.service`, `.socket`, `.timer`, `.mount`, `.target`
- **WantedBy:** which target starts it
- **Restart=:** `on-failure` vs `always` (crash loops)
- **After=/Requires=:** ordering vs hard dependency
- **Type=:** `simple`, `exec`, `forking` (legacy)

```text
systemctl status ssh
systemctl cat ssh
systemctl list-units --failed
systemctl daemon-reload   # after editing a unit
```

A service file is the contract: User, Group, WorkingDirectory, ExecStart, EnvironmentFile, CapabilityBoundingSet, NoNewPrivileges, ProtectSystem.

Timers replace many crons. Prefer `OnCalendar=` + `Persistent=` for job schedules you can `systemctl list-timers`.

## Logs

**journald** is the first stop:

```text
journalctl -u ssh -n 100 --no-pager
journalctl -u myapp --since "1 hour ago"
journalctl -p err -b
```

Traditional files: `/var/log/syslog`, `/var/log/auth.log`, `/var/log/messages` (RHEL). `logrotate` prevents `/var` filling.

App logs: stdout/stderr to journal, or a file under `/var/log/app`. In containers, stdout is the contract for Fluent Bit / ELK.

Never log passwords, tokens, or full authorization headers.

## Resource control

`ulimit -n` (nofile) is a classic “prod worked until traffic.” systemd `LimitNOFILE=`. Containers: `ulimits` in Docker/K8s.

## Checkpoint

Given `systemctl status` inactive (dead): how do you tell “never enabled,” “failed,” and “disabled after install”?
