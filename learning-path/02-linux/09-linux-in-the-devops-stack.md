# Linux in the DevOps stack

Linux is the **runtime** under almost every other tool in this path.

## AWS (module 01)

EC2 is a Linux (or Windows) VM. User-data is cloud-init. SSM Session Manager is SSH with IAM. EBS is a block device you `lsblk` and mount. “Instance status checks” vs “system status checks” vs “app is down” is this module.

## Docker (module 07)

Images are filesystems + a process. `FROM` distro, user in Dockerfile, PID 1 signal handling, `/tmp` space, `ulimit`, `USER` non-root—all Linux. `docker exec` is `nsenter` into namespaces.

## Kubernetes / OpenShift

The **node** is Linux. Pods are cgroups + namespaces. `kubectl debug` often drops you into a Linux userland. Disk pressure, PID pressure, and `NotReady` are node Linux problems, not YAML problems.

## GitLab / Jenkins runners

Runners are Linux VMs or pods. PATH, uid, docker.sock mounts, and workspace permissions are Linux incidents dressed as “pipeline failed.”

## Ansible

Ansible over SSH is remote Linux. Become `sudo`. File modes, SELinux, systemd modules. If you cannot do it by hand, the playbook is a mystery.

## ELK / Fluent Bit

Collectors read `/var/log` and journal. Permissions on log files and journal groups (`systemd-journal`) are why “no logs in Kibana.”

## Prometheus node_exporter

Exposes Linux metrics: load, disk, filesystem, network. Interpreting them is this module.

## Terraform

`remote-exec` and `user_data` are Linux. Prefer cloud-init + images over Terraform SSH.

## Mental picture

```text
Git -> CI runner (Linux) -> image (Linux userland)
  -> node (Linux kernel)
    -> systemd or kubelet
      -> your process
        -> sockets, files, logs
```

If you skip Linux, every later module becomes copy-paste.
