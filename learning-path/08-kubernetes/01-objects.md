# Core objects

**Pod:** smallest deployable; one or more containers; ephemeral IP.

**Deployment:** replica + rollout of Pods.

**Service:** stable DNS/VIP. ClusterIP, NodePort, LoadBalancer.

**ConfigMap/Secret:** config vs sensitive (Secret is still base64, not encryption by itself).

**Probe:** liveness vs readiness vs startup. Readiness gates Service traffic.

**Job/CronJob:** batch.

Declarative: `kubectl apply -f`. Desired vs actual. Controllers reconcile.
