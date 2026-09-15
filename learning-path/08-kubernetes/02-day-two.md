# Day-2 operations

`kubectl describe` events. `logs --previous`. `exec` last resort.

Resources: requests (scheduling) vs limits (throttling/OOM). HPA on CPU or custom metrics.

PDB for voluntary disruption. RollingUpdate maxUnavailable/maxSurge.

NetworkPolicy: default deny in prod namespaces.

Storage: PVC/StorageClass; know AZ stickiness.

Upgrades: version skew kubelet vs apiserver. Drain nodes.
