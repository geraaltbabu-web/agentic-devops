param(
  [string]$BaseUrl = "http://localhost:8080"
)

$health = Invoke-RestMethod -Uri "$BaseUrl/health" -Method Get
if ($health.status -ne "ok") {
  throw "Health check failed: $($health | ConvertTo-Json -Compress)"
}
Write-Host "Smoke test passed: $BaseUrl/health"
