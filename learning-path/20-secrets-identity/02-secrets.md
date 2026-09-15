# Secrets

Sources: Vault, AWS SM, Azure Key Vault. Delivery: env from CSI, file mounts, External Secrets Operator.

Git: SOPS/age encrypted if you must; still prefer runtime inject.

Rotate: dual-valid period. Apps reload or restart.
