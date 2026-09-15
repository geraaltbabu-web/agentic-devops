# Q&A

**Route vs Ingress?** Route is native; TLS edge/passthrough/reencrypt. Ingress still used.

**Why is my pod forbidden to run as root?** SCC/PSA. Fix the image USER, don’t grant `anyuid` casually.

**ROSA vs EKS?** Product vs project: OCP features vs vanilla K8s. Cost, skill, operators.

**oc vs kubectl?** oc understands Routes/Projects; kubectl still works for core objects.
