# CLI cookbook

Use `--output json` in scripts. Use `--query` for humans. Never parse table output.

Set these in every terminal session:

```powershell
$env:AWS_PROFILE = "devops-sandbox"
$env:AWS_REGION = "us-east-1"
aws sts get-caller-identity
```

## Identity

```powershell
aws sts get-caller-identity
aws iam list-account-aliases
aws iam get-role --role-name REPLACE_ROLE
aws iam simulate-principal-policy `
  --policy-source-arn arn:aws:iam::REPLACE_ACCOUNT:role/REPLACE_ROLE `
  --action-names s3:GetObject `
  --resource-arns arn:aws:s3:::REPLACE_BUCKET/hello.txt
```

## S3

```powershell
aws s3api list-buckets
aws s3 ls s3://REPLACE_BUCKET
aws s3 cp .\hello.txt s3://REPLACE_BUCKET/hello.txt
aws s3api get-bucket-policy --bucket REPLACE_BUCKET
aws s3api get-public-access-block --bucket REPLACE_BUCKET
aws s3api list-object-versions --bucket REPLACE_BUCKET
```

Delete a versioned bucket: delete all versions and delete markers, then `delete-bucket`.

## EC2 and VPC

```powershell
aws ec2 describe-vpcs --filters Name=tag:Project,Values=devops-mastery
aws ec2 describe-subnets --filters Name=vpc-id,Values=REPLACE_VPC
aws ec2 describe-route-tables --filters Name=vpc-id,Values=REPLACE_VPC
aws ec2 describe-security-groups --filters Name=vpc-id,Values=REPLACE_VPC
aws ec2 describe-vpc-endpoints --filters Name=vpc-id,Values=REPLACE_VPC
aws ec2 describe-instances --filters Name=tag:Project,Values=devops-mastery
```

## CloudFormation

```powershell
aws cloudformation validate-template --template-body file://labs/vpc.yaml
aws cloudformation deploy --stack-name devops-mastery-vpc --template-file labs/vpc.yaml --parameter-overrides Owner=sandbox
aws cloudformation describe-stack-events --stack-name devops-mastery-vpc --max-items 20
aws cloudformation delete-stack --stack-name devops-mastery-vpc
aws cloudformation wait stack-delete-complete --stack-name devops-mastery-vpc
```

## CloudTrail and CloudWatch

```powershell
aws cloudtrail lookup-events --lookup-attributes AttributeKey=EventName,AttributeValue=CreateBucket --max-results 5
aws logs describe-log-groups
aws cloudwatch describe-alarms
aws cloudwatch set-alarm-state --alarm-name REPLACE_ALARM --state-value ALARM --state-reason "lab"
```

## Cost (read-only)

```powershell
aws ce get-cost-and-usage `
  --time-period Start=2026-09-01,End=2026-09-15 `
  --granularity MONTHLY `
  --metrics UnblendedCost
```

Dates must be real for your account. Do not paste the output into Git.

## SSM (optional Lab 6)

```powershell
aws ssm describe-instance-information
aws ssm start-session --target REPLACE_INSTANCE_ID
```

## Safety aliases

Prefer `--dry-run` where the API supports it (`ec2` often does). There is no dry-run for `s3 rm`. Double-check bucket names.

If a command requires `--no-cli-pager` on Windows to avoid hanging pagers:

```powershell
$env:AWS_PAGER = ""
```
