param(
  [ValidateSet("plan", "deploy", "review", "rollback")]
  [string]$Command = "plan",
  [string]$Environment = "dev",
  [string]$Image = "demo-api:1.1.0",
  [switch]$Apply
)

$env:PYTHONPATH = (Resolve-Path "$PSScriptRoot\..").Path
$argsList = @("-m", "agent", $Command, "--env", $Environment, "--image", $Image, "--json")
if ($Apply) { $argsList += "--apply" }
python @argsList
