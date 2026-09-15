# Kustomize

`kustomization.yaml`: resources + patches + images + namespace. Overlays `dev/` `prod/` that point at a base.

Better than forked YAML copies. Worse than Helm when you need a real package ecosystem. Combination is common: `helm template | kustomize`.
