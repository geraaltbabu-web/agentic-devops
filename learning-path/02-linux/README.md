# 02 — Linux for enterprise DevOps

Goal: use Linux the way platform and SRE teams do: inspect a host, ship a service under systemd, read logs, debug the network, automate with Bash, and recover from the failures that actually page people.

You do **not** need to become a kernel developer. You do need to be faster than “reboot it” on a box that is out of disk, DNS-broken, or stuck in a crash loop.

## Before you begin

Recommended lab environment (pick one):

1. **WSL2 Ubuntu 24.04** on Windows (fits this machine)
2. Ubuntu 24.04 VM
3. A throwaway AWS EC2 instance from module 01 (stop/terminate after class)

Do not practice `rm -rf`, firewall changes, or user deletion on a work laptop’s only OS. WSL or a VM is the blast-radius boundary.

You need: `bash`, `sudo` in the lab OS, Git, and an editor. Optional: `jq`, `curl`, `python3`.

## Learning sequence

0. [Study plan](00-study-plan.md)
1. [Foundations: what Linux is in production](01-foundations.md)
2. [Users, files, permissions, disks](02-users-files-disks.md)
3. [Processes, systemd, and logs](03-processes-systemd-logs.md)
4. [Networking, DNS, TLS from the host](04-host-networking.md)
5. [Bash for operators](05-bash-for-operators.md)
6. [Enterprise operations and hardening](06-enterprise-ops.md)
7. [Real-world Q&A](07-real-world-q-and-a.md)
8. [Command cookbook](08-cli-cookbook.md)
9. [Linux in the DevOps stack](09-linux-in-the-devops-stack.md)
10. [Labs](labs/README.md)
11. [Capstone](capstone.md)

## Competency checkpoints

After this module you should be able to:

- Explain kernel vs user space, distro vs kernel, and why containers still share a kernel
- Navigate FHS (`/etc`, `/var`, `/usr`, `/proc`, `/sys`) and find *why* a file is where it is
- Diagnose disk full, inode full, permission denied, and “file not found” that is actually `PATH` or cwd
- Read `systemctl`, unit files, restart policies, and `journalctl` without guessing
- Use `ss`, `ip`, `/etc/resolv.conf` vs systemd-resolved, and curl `-v` to prove a hop failed
- Write a small idempotent Bash check script with `set -euo pipefail`, quoting, and no secrets in logs
- Describe SSH, sudo, umask, capabilities, and why root SSH is banned
- Map Linux skills onto EC2, Docker, Kubernetes nodes, and OpenShift workers

## Safety

1. Prefer read-only commands first (`ls`, `stat`, `systemctl status`, `journalctl --since`).
2. Never paste passwords, private keys, or `/etc/shadow` into Git.
3. Treat `sudo` as a change ticket: know the blast radius.
4. On WSL, some systemd/network features differ from a full VM. Labs note that.

## Evidence of completion

Keep private notes of commands and outputs. Do not commit hostnames that identify an employer, or SSH private keys. Sanitized transcripts are fine.
