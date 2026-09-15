# Command cookbook

Run these **read-only** first. Distro: Ubuntu/Debian unless noted.

Pager off:

```bash
export SYSTEMD_PAGER=cat
```

## Who and where

```bash
uname -a
hostnamectl
id
pwd
df -h
df -i
lsblk
```

## Files

```bash
ls -la /var/log
stat /etc/hosts
readlink -f .
find /var/log -type f -size +50M
du -xh -d 1 /var 2>/dev/null | sort -h | tail
```

## Processes

```bash
ps aux --sort=-%mem | head
pgrep -a sshd
ls -l /proc/$(pgrep -d, -x sshd | cut -d, -f1)/fd 2>/dev/null | head
```

## systemd / journal

```bash
systemctl is-system-running || true
systemctl list-units --type=service --state=failed
journalctl -p err -n 50 --no-pager
```

On WSL without systemd, skip `systemctl` and use `ps` + log files.

## Network

```bash
ip -br addr
ip route
ss -lntup
resolvectl status 2>/dev/null || cat /etc/resolv.conf
curl -sS -o /dev/null -w "%{http_code} %{time_total}\n" --max-time 5 https://example.com
```

## Packages (Ubuntu)

```bash
apt list --installed 2>/dev/null | wc -l
apt-cache policy bash
```

Do not run `apt upgrade` in the lab unless you intend to change the lab VM.

## Users

```bash
getent passwd | tail
sudo -n true && echo "passwordless sudo" || echo "sudo needs a password or is missing"
```
