# Q&A

**Image vs container?** Immutable template vs running instance.

**Why not latest?** Non-deterministic deploys and rollbacks.

**Bind-mount docker.sock?** Effectively root on the host. Avoid in untrusted CI.

**CrashLoop from OOM?** Limits vs leaks; `docker stats`.

**Multi-stage?** Build tools in stage 1; copy artifact to runtime stage.
