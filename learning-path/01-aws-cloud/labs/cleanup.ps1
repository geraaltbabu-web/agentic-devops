$ErrorActionPreference = "Stop"
$env:AWS_PAGER = ""

aws sts get-caller-identity | Out-Null

$stacks = @(
  "devops-mastery-vpc",
  "devops-mastery-alarm"
)

foreach ($name in $stacks) {
  $exists = aws cloudformation describe-stacks --stack-name $name 2>$null
  if ($LASTEXITCODE -eq 0 -and $exists) {
    Write-Host "Deleting $name"
    aws cloudformation delete-stack --stack-name $name
    aws cloudformation wait stack-delete-complete --stack-name $name
  }
  else {
    Write-Host "Skip missing $name"
  }
}

Write-Host "Cleanup finished. Check Cost Explorer tomorrow."
