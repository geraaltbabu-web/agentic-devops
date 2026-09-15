# Hardening checklist (lab OS only)

Do not apply blindly to a host you cannot recover.

- [ ] Unique hostname; documented
- [ ] Time sync (`timedatectl`)
- [ ] Unattended upgrades *or* an image pipeline — pick one and know it
- [ ] No password SSH; keys or SSM
- [ ] Root SSH disabled (after your user can sudo)
- [ ] `ufw`/`nftables` default deny inbound except what you need
- [ ] Disk alerts on `/` and `/var`
- [ ] journald/logrotate so logs cannot fill the root FS
- [ ] Separate service user for apps; no app as root
- [ ] `fail2ban` or equivalent only if you expose SSH to the internet (prefer not to)
- [ ] Cloud SG: no `0.0.0.0/0` to 22
- [ ] Backup/rebuild story: AMI or golden image, not “we will remember packages”

WSL: skip SSH daemon changes if you do not use `sshd` on WSL.
