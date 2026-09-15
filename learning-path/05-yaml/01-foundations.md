# Foundations

**JSON:** strict, easy for APIs and `jq`. No comments (usually).

**YAML:** comments, anchors (`&`, `*`), nested K8s/Helm/Ansible/GitHub Actions. Footguns: `on: yes` becomes boolean; Norway problem (`NO`); tabs vs spaces; duplicate keys.

**Rules:** 2-space indent; quote strings that look like booleans/versions (`"1.10"`); validate in CI (`yamllint`, `kubeconform`, `actionlint`).

**jq** for JSON. **yq** for YAML. Prefer generating YAML from a typed language if the file is huge.

Schema: Kubernetes OpenAPI, JSON Schema for your values files. Invalid config should fail the PR, not prod.
