# Foundations: what Linux is in production

## Mental model

A Linux host is:

```text
Hardware or hypervisor
  -> kernel (processes, memory, filesystems, network stack, cgroups)
    -> user space (systemd, sshd, your app, shells)
```

**Distro** (Ubuntu, RHEL, Amazon Linux) is packages, defaults, and support lifecycle. **Kernel** is the thing containers on one node all share. That is why a kernel CVE can hit every pod on a node.

DevOps uses Linux as:

- the OS on VMs (EC2, vSphere)
- the OS inside containers (often distroless or Alpine/Debian slim)
- the OS on Kubernetes/OpenShift workers
- the OS of CI runners
- the place `systemd`, `journald`, and `iptables`/`nftables` still matter even when you “only do containers”

## Kernel vs user space (operator view)

| You feel this | It usually lives here |
|---------------|------------------------|
| Process scheduling, OOM killer | Kernel |
| Listening sockets, routing | Kernel + `ip`/`ss` |
| “Service failed to start” | systemd + unit + app |
| Package version | Distro (`apt`/`dnf`) |
| Container isolation | Namespaces + cgroups (kernel) |

`/proc` and `/sys` are kernel APIs mounted as files. `cat /proc/meminfo` is not a text file on disk; it is a live kernel dump.

## Filesystem Hierarchy Standard (FHS)

Memorize by *purpose*:

| Path | Purpose |
|------|---------|
| `/` | Root of this mount namespace |
| `/bin`, `/usr/bin` | User commands |
| `/sbin`, `/usr/sbin` | Admin commands |
| `/etc` | Host configuration (treat as code + backup) |
| `/var` | Variable data: logs, spool, some app state |
| `/var/log` | Traditional logs (plus journal) |
| `/home` | People |
| `/root` | Root’s home |
| `/tmp`, `/var/tmp` | Temporary; `/tmp` often tmpfs |
| `/opt` | Optional third-party software |
| `/srv` | Data for services (less used in cloud) |
| `/proc` | Processes and kernel |
| `/sys` | Devices, cgroups |
| `/dev` | Device nodes |
| `/boot` | Kernel and bootloader (VMs; not in most containers) |

When disk is full, look at `/var` first, then Docker/container dirs, then journal.

## Shell, terminal, and remote

- **Shell:** `bash` in this course (enterprise still has a lot of Bash)
- **Login vs non-login, interactive vs not:** CI scripts are non-interactive; your `~/.bashrc` may not run
- **SSH:** encrypted remote shell; keys not passwords; jump hosts / SSM in AWS
- **TTY:** why `systemctl` asks for a pager and CI hangs without `SYSTEMD_PAGER=`

## Package managers

| Family | Install | Search |
|--------|---------|--------|
| Debian/Ubuntu | `apt` | `apt search` |
| RHEL/Amazon Linux | `dnf` | `dnf search` |

Pin versions in golden images. `apt upgrade` on a lone prod box without a tested image pipeline is how you get “it was only a patch.”

## Cloud-init and first boot

VMs in AWS/GCP/Azure almost always run **cloud-init**: SSH keys, hostname, packages, user-data. If user-data fails, the instance looks “up” but the app never installed. Check `/var/log/cloud-init-output.log`.

## Checkpoint

- Why a container can see a different `/etc` but the same kernel
- Difference between `/usr/bin` and `/usr/local/bin`
- Why CI Bash does not load your aliases
