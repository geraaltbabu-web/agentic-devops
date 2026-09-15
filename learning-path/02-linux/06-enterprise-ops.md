# Enterprise operations and hardening

## Golden images

Enterprises do not “apt install on Friday in prod.” Flow:

```text
Packer or image pipeline -> AMI / VM template / node image
  -> CIS-ish baseline
  -> agents (SSM, logging, AV as required)
  -> immutability: replace, don't patch-in-place when you can
```

Emergency CVE: rebuild image, rolling replace. SSH in and `yum update` is last resort.

## SSH standard

- Key auth only; disable password auth
- Disable root login
- `AllowGroups` / Identity Center / SSM instead of standing bastions when possible
- `AuthorizedKeysCommand` or `sshd` Match blocks in advanced setups
- Record session if compliance requires (SSM, teleports, etc.)

Host keys: `known_hosts`. Pin or use a CA. Blind `StrictHostKeyChecking=no` is a lab-only sin.

## sudo standard

- Named commands, not `ALL=(ALL) NOPASSWD: ALL` for humans
- Break-glass documented
- `sudo -l` to see what you actually have

## Patch and inventory

- Know kernel (`uname -r`) vs userspace
- `needs-restarting` / `/var/run/reboot-required`
- Live kernel patching exists; it is not a substitute for a reboot policy

## SELinux / AppArmor

Enforcing MAC will deny a correctly chmod’d file. Do not `setenforce 0` as the fix. Use audit logs, then a **minimal** module or file context.

Ubuntu default is AppArmor. RHEL default is SELinux.

## Time, locale, hostname

Hostname must match inventory and certs. `hostnamectl`. Cloud-init may reset it.

## Capacity and performance snapshot

When “it is slow”:

1. `uptime` load vs CPU count
2. `free -h` / swapping
3. `df -h` / `df -i`
4. `iostat -xz 1` (if sysstat installed)
5. `ss -s` connection counts
6. app logs / traces

Load average high with idle CPU can be **uninterruptible disk wait** (D state).

## Runbooks

Same as AWS module: impact, severity, evidence, mitigate, verify, communicate, prevent. Linux is often the evidence layer for a cloud incident.

## Checkpoint

Write a 10-line hardening checklist you would apply to a new Ubuntu AMI before it sees a public SG.
