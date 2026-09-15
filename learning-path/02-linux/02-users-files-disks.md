# Users, files, permissions, disks

## Users and groups

- `/etc/passwd`: user, UID, GID, home, shell
- `/etc/group`: groups
- `/etc/shadow`: password hashes (root only; never copy out)
- `id`, `whoami`, `getent passwd`

**UID 0 is root.** Service users should be UID >= 1000 or distro system ranges, **no login shell** (`/usr/sbin/nologin`).

`sudo` is “run as another user with an audit trail.” `/etc/sudoers` and `/etc/sudoers.d/`. Use `visudo`. Never `chmod 777` to “fix sudo.”

## Permissions

Classic mode: owner / group / other × rwx.

```text
rwxr-xr-x  user group  file
```

- Files: `x` means execute
- Directories: `x` means you may *enter* the directory; `r` means you may list
- `suid`/`sgid`/`sticky` (`/tmp` sticky bit): know they exist; do not sprinkle suid binaries

`umask` controls default mode. `022` is common; more open umask leaks files.

ACLs (`getfacl`/`setfacl`) appear in enterprises sharing filesystems. If `ls -l` shows `+`, ACLs are in play.

## Ownership and the real “permission denied”

Check in order:

1. Path components: every directory to the file needs `x`
2. File mode and owner
3. Mount options (`noexec`, `nosuid`, NFS `root_squash`)
4. SELinux/AppArmor denials (`ausearch`, `dmesg`, `journalctl`)
5. Immutable attr (`lsattr`/`chattr +i`)

## Links and inodes

- **Hard link:** same inode, same filesystem
- **Symlink:** pointer; can dangle
- Disk full vs **inode** full: `df -h` vs `df -i`

A million tiny files in a cache dir fills inodes while `df -h` still looks fine.

## Disks, mounts, LVM

```text
lsblk
df -hT
findmnt
```

LVM: PV → VG → LV. Snapshots exist; they are not a backup strategy by themselves.

Swap: if the host is swapping hard, latency is already bad. Don’t “add swap to hide a memory leak” in prod without a plan.

## Special files

- Named pipes, sockets, device nodes
- `/dev/null`, `/dev/zero`, `/dev/urandom`
- Here-docs and redirection: `>`, `>>`, `2>&1`, `tee`

## Checkpoint

Explain why `chmod 777 /var/app` is both a security incident and usually not the actual fix for a service user that cannot write its log directory.
