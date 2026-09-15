# Foundations

Container = namespaces + cgroups + a filesystem snapshot. **Same kernel as the host.**

Image = layers. Changing a late COPY invalidates cache below. Order: deps then source.

Run: `docker run --rm -p 8080:8080 --read-only` when you can. Mount secrets as files, not ENV, if possible.

PID 1: your process must handle SIGTERM (Python default is ok-ish; shell PID 1 is not). Prefer `exec` form CMD JSON.

User: never root in prod images. Numeric UID for K8s `runAsNonRoot`.
