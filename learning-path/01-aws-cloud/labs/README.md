# Hands-on labs

Use a personal sandbox only. Run labs in order and clean up after each session.

## Lab 0 — account and CLI

1. Enable root MFA and remove root access keys.
2. Create a budget alert in Billing.
3. Configure AWS CLI SSO.
4. Run:

```powershell
aws sts get-caller-identity
aws configure get region
aws ec2 describe-regions --query "Regions[].RegionName" --output table
```

Success: you can identify the account, role session, and selected Region without exposing the output publicly.

## Lab 1 — read-only inventory

Install `boto3`, then run the inventory script:

```powershell
python -m pip install boto3
python .\labs\inventory.py --region us-east-1
```

Study pagination, SDK sessions, exception handling, and why automation should emit machine-readable output.

## Lab 2 — secure S3

Create a unique bucket:

```powershell
$Bucket = "devops-mastery-$((aws sts get-caller-identity --query Account --output text))-$((Get-Random))"
aws s3api create-bucket --bucket $Bucket --region us-east-1
aws s3api put-public-access-block --bucket $Bucket --public-access-block-configuration `
  BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
aws s3api put-bucket-versioning --bucket $Bucket --versioning-configuration Status=Enabled
"hello from AWS learning" | Set-Content hello.txt
aws s3 cp hello.txt "s3://$Bucket/hello.txt"
aws s3api head-object --bucket $Bucket --key hello.txt
```

Cleanup all versions before deleting the bucket. Never make the bucket public.

## Lab 3 — free VPC with CloudFormation

This creates a VPC, public and private subnets, routing, security group, and S3 gateway endpoint. It deliberately creates **no NAT Gateway or EC2 instance**.

```powershell
aws cloudformation validate-template --template-body file://labs/vpc.yaml
aws cloudformation deploy `
  --stack-name devops-mastery-vpc `
  --template-file labs/vpc.yaml `
  --parameter-overrides Owner=$env:USERNAME
aws cloudformation describe-stacks --stack-name devops-mastery-vpc
```

Trace each route. Explain why the private subnet has no internet access and how its S3 endpoint works.

Cleanup:

```powershell
aws cloudformation delete-stack --stack-name devops-mastery-vpc
aws cloudformation wait stack-delete-complete --stack-name devops-mastery-vpc
```

## Lab 4 — IAM policy reasoning

Read `readonly-s3-policy.json`. For every statement, identify principal source, action, resource, condition, and blast radius. Use IAM Policy Simulator in your sandbox. Do not attach experimental policies to production identities.

## Lab 5 — CloudTrail investigation

Perform a tagged S3 API call, then find it in CloudTrail Event History. Identify event source, event name, caller, source IP, Region, request parameters, response, and error code.

## Lab 6 — optional EC2 and Systems Manager

This may incur charges. Launch only a currently free-tier-eligible instance in a public sandbox subnet, with:

- no inbound security-group rules
- an instance role containing `AmazonSSMManagedInstanceCore`
- encrypted root volume
- IMDSv2 required
- ownership and expiry tags

Connect with Session Manager, inspect systemd and logs, then terminate the instance and delete its role/profile/security group.

## Lab 7 — OIDC design (no AWS spend)

1. Read `oidc-trust-policy.example.json` and `github-actions-oidc.example.yml`.
2. Rewrite the `sub` condition for:
   - pull requests (plan only)
   - `environment:staging`
   - `environment:prod` plus a required reviewer
3. List the exact IAM actions a **plan role** vs **apply role** need for CloudFormation + S3 + ECS (or EKS). Keep them separate.
4. Explain what happens if `sub` is `repo:my-org/*`.

No credentials. No live GitHub OIDC provider required.

## Lab 8 — CloudWatch alarm (cheap)

Create a metric alarm on a custom metric you put:

```powershell
aws cloudwatch put-metric-data --namespace DevOpsMastery --metric-name LabHeartbeat --value 1
aws cloudformation deploy --stack-name devops-mastery-alarm --template-file labs/cloudwatch-alarm.yaml
```

Force it to ALARM, confirm the state, then delete the stack.

## Lab 9 — cleanup drill

Run `.\labs\cleanup.ps1` after replacing the stack names if you changed them. Confirm no `devops-mastery` stacks remain:

```powershell
aws cloudformation list-stacks --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE
```

Do not paste account-specific output into Git.

## Completion gate

You are ready for the capstone when you can recreate the VPC, explain every route and IAM decision, prove cleanup, and diagnose an intentional security-group or permission failure without granting broad access.
