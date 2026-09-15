# Enterprise

- Tag: `app:git-abc123` and digest `sha256:...`
- SBOM + scan on push (Trivy/Grype)
- Distroless or slim; no compilers in runtime
- Supply chain: pin FROM digest
- Runtime: resource limits, drop caps, no `--privileged` unless you can defend it
- Log to stdout; JSON if possible
- Compose for local (this repo’s banking compose); not for prod HA
