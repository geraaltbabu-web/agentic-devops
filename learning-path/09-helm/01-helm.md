# Helm

Chart = templates + default values. Release = named install in a namespace.

`helm template` is the PR check. `helm upgrade --install` is apply. `--atomic` / `--wait` for safer CD.

Values hierarchy: chart default → env file → `--set` (avoid `--set` in prod; it is invisible).

Version the chart independently from appVersion. Pin chart versions in GitOps.
