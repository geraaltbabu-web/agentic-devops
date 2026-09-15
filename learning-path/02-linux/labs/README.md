# Labs

Use WSL Ubuntu, a VM, or a disposable cloud instance. Commands assume Bash.

```bash
cd learning-path/02-linux/labs
chmod +x ./*.sh
```

## Lab 0 — prove the lab OS

```bash
./00-lab-os.sh
```

Expect: kernel, distro, user, disk, whether systemd is available.

## Lab 1 — files and permissions

```bash
./01-permissions.sh
```

Creates a temp dir, a service-like user file layout, and shows a **wrong** `777` vs a correct owner/mode. Cleans up unless you export `KEEP=1`.

## Lab 2 — disk and inodes

```bash
./02-disk.sh
```

Shows `df -h` vs `df -i` and a tiny-file demo in a temp dir (capped; safe).

## Lab 3 — processes and (optional) systemd

```bash
./03-process.sh
```

This lab is written for Git Bash, WSL, and Ubuntu. On Windows Git Bash, `python3` may be missing (`python` works if the Store alias is disabled) and `ps -o` may be unavailable — the script degrades.

If `systemctl` works:

```bash
# read-only
systemctl list-units --type=service --state=running | head
```

## Lab 4 — network from the host

```bash
./04-network.sh
```

Prints routes, listeners, and a timed `curl` to `https://example.com`. Failures are acceptable on air-gapped hosts; read the script output.

## Lab 5 — operator health check script

```bash
./05-healthcheck.sh
./05-healthcheck.sh --json
```

This is the pattern you will reuse in CI and on nodes.

## Lab 6 — hardening checklist (manual)

Go through `hardening-checklist.md` on your **lab** OS only. Check items; do not lock yourself out of WSL. Skip SSH changes on a machine you only access via SSH until you have a second session.

## Cleanup

Scripts use `/tmp/devops-mastery-linux-*`. Reboot or `rm -rf /tmp/devops-mastery-linux-*` if a script was killed mid-run.

## Completion gate

You can explain every field you printed, reproduce a permission failure on purpose, and restore it without `777`.
