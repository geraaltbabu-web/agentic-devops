# Templating

**Helm:** Go templates + values. `helm template` in PRs. `required` on critical values. No `{{ .Values.password }}` in Git—use external secrets.

**Kustomize:** patches and overlays without a Turing-complete template. Good for env folders.

**Jinja2:** Ansible, some Python tools. Autoescape for HTML only; YAML still needs quoting.

**envsubst / sed:** last resort. Unquoted `sed` on manifests is an incident waiting.

Render in CI and **diff against last good render** for GitOps repos.
