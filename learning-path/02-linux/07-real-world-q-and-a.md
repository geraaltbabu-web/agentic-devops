# Real-world questions and answers

Answer aloud first. Include how you would **verify**.

## Foundations

**Kernel vs distro?**  
Kernel: scheduling, memory, filesystems, network, cgroups. Distro: packages, systemd units, support window, defaults. Containers share the **node kernel**.

**Why can I not run `systemctl` usefully in some containers?**  
No systemd as PID 1, or you are in a minimal namespace. Debug the **node** or use the runtime’s logs (`docker logs`, `kubectl logs`).

**What is `/proc`?**  
A kernel interface, not a normal disk filesystem. Killing disk “cleanup” of `/proc` is nonsense.

## Files and identity

**`Permission denied` on a file with `644`?**  
A parent directory lacks `x`, or MAC (SELinux), or mount `noexec` (for scripts), or you are not who you think (`id`).

**Disk full but `du` does not add up?**  
Deleted files still open (`lsof +L1`), or inode exhaustion (`df -i`), or a mount hiding a directory.

**Why not `chmod 777`?**  
World-writable dirs invite symlink and write attacks; you also failed to identify the service user. Fix owner/group and `750`/`640` as appropriate.

## Processes and systemd

**When is `kill -9` acceptable?**  
When the process ignores TERM after a defined timeout and you accept unclean shutdown. systemd `TimeoutStopSec` then SIGKILL is the controlled form.

**`Restart=always` and a crash loop.**  
systemd will restart forever. Use `StartLimitBurst` / `StartLimitInterval`, fix the app, watch journal. Crash loops hide behind “service is active.”

**Where did stdout go?**  
If `StandardOutput=journal`, `journalctl -u`. If file, unit `StandardOutput=file:` or app config. In K8s, the runtime.

## Networking

**Nothing listens on 8080 but the unit is active.**  
Wrong `ExecStart`, app bound to another port, failed after fork (`Type=` mismatch), or still starting. `ss -lntp` + journal.

**DNS works with `dig` but not the app.**  
App uses different resolver, hard-coded IP, `/etc/nsswitch.conf`, or IPv6 first timeout. `getent hosts` matches libc better than `dig`.

**Host firewall is open, still blocked.**  
Cloud SG/NACL, NSG, iptables in another table, kube-proxy, docker iptables. Name the layer.

## Bash

**Why did `rm $files` destroy extra paths?**  
Word splitting and globbing. Quote and use arrays. `set -f` is not a substitute for quoting.

**Cron job works in SSH but not in cron.**  
`PATH`, cwd, missing env, no TTY, secrets only in `.bashrc`. Use absolute paths and `Environment=` in a systemd timer.

## Security

**Why disable root SSH?**  
Shared root has no attribution; stolen key is full host. Use sudo + named users or SSM.

**AppArmor denied vs chmod.**  
MAC is extra. Read the denial; restore context or add a profile. Do not disable globally.

## Self-score

Same rule as AWS: identity, verification, security, blast radius. If you cannot order a hung `curl` debug sequence, restudy chapter 4.
