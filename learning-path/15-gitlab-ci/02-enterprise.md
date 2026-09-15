# Enterprise

Protected branches + protected variables. Environment `production` needs approvers.

OIDC to AWS (`CI_JOB_JWT` / federation). Don’t put long-lived keys in CI/CD variables if OIDC works.

Runners: autoscale on K8s/EC2. Isolate privileged docker-in-docker.
