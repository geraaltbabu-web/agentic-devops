# Platform differences

| K8s | OpenShift |
|-----|-----------|
| Namespace | Project |
| Ingress | Route (and Ingress) |
| kubectl | oc (superset) |
| PSA/PSP history | SCC (and newer PSA) |
| Ingress controller choice | Router |

Builds: BuildConfig/S2I exist; many teams still build in GitHub Actions and only deploy.

Operators: OLM. Don’t install random operators in prod without an owner.

Auth: OAuth, IDP (SAML/OIDC), kubeadmin is not a strategy.
