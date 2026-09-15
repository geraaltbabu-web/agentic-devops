"""Read-only AWS inventory. It deliberately prints no credentials or secret values."""

from __future__ import annotations

import argparse
import json

import boto3
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError


def collect(region: str) -> dict:
    session = boto3.Session(region_name=region)
    sts = session.client("sts").get_caller_identity()
    ec2 = session.client("ec2")
    instances = []
    paginator = ec2.get_paginator("describe_instances")
    for page in paginator.paginate(
        Filters=[{"Name": "tag:Project", "Values": ["devops-mastery"]}]
    ):
        for reservation in page["Reservations"]:
            for item in reservation["Instances"]:
                instances.append(
                    {
                        "id": item["InstanceId"],
                        "state": item["State"]["Name"],
                        "type": item["InstanceType"],
                        "az": item["Placement"]["AvailabilityZone"],
                    }
                )

    buckets = [item["Name"] for item in session.client("s3").list_buckets()["Buckets"]]
    return {
        "identity": {
            "account": sts["Account"],
            "principal_arn": sts["Arn"],
        },
        "region": region,
        "tagged_instances": instances,
        "bucket_count": len(buckets),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--region", default="us-east-1")
    args = parser.parse_args()
    try:
        print(json.dumps(collect(args.region), indent=2))
        return 0
    except (NoCredentialsError, BotoCoreError, ClientError) as exc:
        print(json.dumps({"error": type(exc).__name__, "message": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
