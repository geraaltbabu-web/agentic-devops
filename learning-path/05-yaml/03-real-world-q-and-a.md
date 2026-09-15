# Q&A

**Why did `on: no` break GitHub Actions?** YAML boolean. Quote `"on"`.

**Helm vs Kustomize?** Helm packages a product; Kustomize patches a tree. Often Helm chart + Kustomize overlay or Argo Helm.

**How to hide a secret in values.yaml?** You do not. Reference a Secret name; inject at runtime.

**Duplicate keys in YAML?** Last one wins in many parsers—silent bug. yamllint.
