# Foundations and account setup

## Mental model

AWS is a set of regional and global APIs. The console, CLI, SDKs, Terraform, and CI/CD systems all call those APIs. DevOps engineers automate desired state, control identity, observe outcomes, and recover safely.

- **Region:** geographic API boundary, such as `us-east-1`
- **Availability Zone:** isolated data-center group inside a Region
- **Edge location:** CloudFront/Route 53 edge infrastructure
- **Account:** strongest billing, quota, and blast-radius boundary
- **VPC:** regional private network boundary
- **ARN:** unique identifier for an AWS resource
- **Tag:** key/value metadata used for ownership, automation, policy, and cost

AWS secures the cloud; you secure what you configure in the cloud. Managed services reduce—but never remove—your responsibility.

## Secure bootstrap

1. Create a dedicated sandbox account.
2. Enable root MFA and store recovery details securely.
3. Do not create root access keys.
4. Configure alternate security and billing contacts.
5. Enable IAM Identity Center for human access.
6. Create an administrator permission set for initial setup; use a lower-privilege role for daily work.
7. Create a monthly budget and alerts at low thresholds.
8. Enable CloudTrail, GuardDuty, and AWS Config when budget permits.
9. Block public S3 access at account level.
10. Choose one home Region and deny unused Regions where practical.

## Install and verify the CLI

```powershell
aws --version
aws configure sso
aws sso login --profile devops-sandbox
$env:AWS_PROFILE = "devops-sandbox"
$env:AWS_REGION = "us-east-1"
aws sts get-caller-identity
aws configure list
```

Prefer SSO or workload identity. `aws configure` with long-lived access keys is retained mainly for legacy systems.

## How AWS authorization works

An API request is allowed only after AWS evaluates all relevant policy layers:

1. Organization service control policies
2. Resource control policies
3. Identity policies and permission boundaries
4. Session policies
5. Resource policies
6. Explicit denies

An explicit deny wins. Otherwise an applicable allow is required.

Use this troubleshooting order:

1. Confirm the caller: `aws sts get-caller-identity`
2. Confirm Region and account
3. Read the denied action and resource ARN
4. Check identity policy, resource policy, permission boundary, SCP, and KMS policy
5. Check session tags and conditions
6. Use CloudTrail to inspect the request
7. Fix the narrow cause—never attach `AdministratorAccess` as a shortcut

## CLI habits used in enterprises

```powershell
# Query only what you need
aws ec2 describe-instances `
  --filters "Name=tag:Project,Values=devops-mastery" `
  --query "Reservations[].Instances[].{Id:InstanceId,State:State.Name,Type:InstanceType}" `
  --output table

# Use pagination-safe SDK/CLI behavior; do not parse human table output in scripts
aws s3api list-buckets --query "Buckets[].Name" --output json

# Generate a CLI skeleton before a risky call
aws ec2 run-instances --generate-cli-skeleton input > request.json
```

Production automation should be idempotent, tagged, logged, retry-aware, and safe when interrupted.

## Checkpoint

Explain without notes:

- Why accounts are better isolation boundaries than VPCs
- Why IAM users are discouraged for humans and CI/CD
- Why `AccessDenied` can persist even when an identity policy contains `Allow`
- Which services are global and which are regional
- How you prove which identity and Region a script is using
