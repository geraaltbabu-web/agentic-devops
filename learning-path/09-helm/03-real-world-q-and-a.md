# Q&A

**Why is --set password= in CI logs bad?** Process list and logs. Use locked values files + external secrets.

**Chart museum vs OCI?** OCI (GHCR/ECR) is the current default direction.

**Failed upgrade leftover?** `helm history`, `rollback`. `--atomic` deletes on fail.
