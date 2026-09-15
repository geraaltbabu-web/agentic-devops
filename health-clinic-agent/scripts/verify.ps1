$ErrorActionPreference = "Stop"
Set-Location (Resolve-Path "$PSScriptRoot\..")
$env:PYTHONPATH = (Get-Location).Path

python -m pip install pytest -q
python -m pytest -q
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

python -m agent plan --env staging --image clinic-api:1.1.0
exit $LASTEXITCODE
