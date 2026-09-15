$ErrorActionPreference = "Stop"
Set-Location (Resolve-Path "$PSScriptRoot\..")

Write-Host "1/4 Python tests"
python -m unittest discover -s tests -v
if ($LASTEXITCODE) { exit $LASTEXITCODE }

Write-Host "2/4 Deployment-agent plan"
python agent/deploy_agent.py --environment staging --image ghcr.io/demo/banking:1.0.0
if ($LASTEXITCODE) { exit $LASTEXITCODE }

Write-Host "3/4 Docker Compose syntax"
docker compose config --quiet
if ($LASTEXITCODE) { exit $LASTEXITCODE }

Write-Host "4/4 Optional tools"
if (Get-Command terraform -ErrorAction SilentlyContinue) {
  terraform -chdir=infra/terraform init -backend=false
  terraform -chdir=infra/terraform validate
}
if (Get-Command helm -ErrorAction SilentlyContinue) {
  helm lint platform/chart -f platform/environments/dev.yaml
}
Write-Host "Verification complete."
