# Labs

If Helm is installed:

```bash
helm lint ../../../banking-platform/platform/chart
helm template demo ../../../banking-platform/platform/chart -f ../../../banking-platform/platform/environments/dev.yaml | head
```

Otherwise read those files and list every template object (Deploy, SVC, HPA, Route, NetworkPolicy).
