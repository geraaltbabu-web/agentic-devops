terraform {
  required_version = ">= 1.7.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" { region = var.aws_region }

data "aws_caller_identity" "current" {}
data "aws_partition" "current" {}
data "aws_availability_zones" "available" { state = "available" }

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"
  name    = "${var.project}-${var.environment}"
  cidr    = var.vpc_cidr
  azs     = slice(data.aws_availability_zones.available.names, 0, 3)
  private_subnets = [for i in range(3) : cidrsubnet(var.vpc_cidr, 4, i)]
  public_subnets  = [for i in range(3) : cidrsubnet(var.vpc_cidr, 4, i + 8)]
  enable_nat_gateway = true
  single_nat_gateway = var.environment != "prod"
  enable_dns_hostnames = true
  tags = local.tags
}

resource "aws_kms_key" "platform" {
  description             = "Synthetic banking platform"
  deletion_window_in_days = 10
  enable_key_rotation     = true
  tags                    = local.tags
}

resource "aws_ecr_repository" "services" {
  for_each             = toset(var.services)
  name                 = "${var.project}/${each.value}"
  image_tag_mutability = "IMMUTABLE"
  encryption_configuration {
    encryption_type = "KMS"
    kms_key          = aws_kms_key.platform.arn
  }
  image_scanning_configuration { scan_on_push = true }
  tags = local.tags
}

resource "aws_s3_bucket" "audit" {
  bucket_prefix = "${var.project}-${var.environment}-audit-"
  force_destroy = var.environment != "prod"
  tags          = local.tags
}
resource "aws_s3_bucket_versioning" "audit" {
  bucket = aws_s3_bucket.audit.id
  versioning_configuration { status = "Enabled" }
}
resource "aws_s3_bucket_server_side_encryption_configuration" "audit" {
  bucket = aws_s3_bucket.audit.id
  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.platform.arn
      sse_algorithm     = "aws:kms"
    }
  }
}
resource "aws_s3_bucket_public_access_block" "audit" {
  bucket = aws_s3_bucket.audit.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_security_group" "opensearch" {
  name_prefix = "${var.project}-${var.environment}-search-"
  vpc_id      = module.vpc.vpc_id
  ingress {
    description = "HTTPS from platform VPC"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = local.tags
}

# Managed OpenSearch is the production ELK-compatible log store.
resource "aws_opensearch_domain" "logs" {
  domain_name    = "${var.project}-${var.environment}"
  engine_version = "OpenSearch_2.15"
  access_policies = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        AWS = "arn:${data.aws_partition.current.partition}:iam::${data.aws_caller_identity.current.account_id}:root"
      }
      Action   = "es:*"
      Resource = "arn:${data.aws_partition.current.partition}:es:${var.aws_region}:${data.aws_caller_identity.current.account_id}:domain/${var.project}-${var.environment}/*"
    }]
  })
  cluster_config {
    instance_type          = var.environment == "prod" ? "m6g.large.search" : "t3.small.search"
    instance_count         = var.environment == "prod" ? 3 : 1
    zone_awareness_enabled = var.environment == "prod"
    dynamic "zone_awareness_config" {
      for_each = var.environment == "prod" ? [1] : []
      content { availability_zone_count = 3 }
    }
  }
  vpc_options {
    subnet_ids         = var.environment == "prod" ? module.vpc.private_subnets : [module.vpc.private_subnets[0]]
    security_group_ids = [aws_security_group.opensearch.id]
  }
  ebs_options {
    ebs_enabled = true
    volume_size = 20
    volume_type = "gp3"
  }
  encrypt_at_rest {
    enabled    = true
    kms_key_id = aws_kms_key.platform.arn
  }
  node_to_node_encryption { enabled = true }
  domain_endpoint_options {
    enforce_https       = true
    tls_security_policy = "Policy-Min-TLS-1-2-2019-07"
  }
  tags = local.tags
}

# ROSA Hosted Control Plane is managed OpenShift on AWS. ROSA CLI performs
# account-role/OIDC setup in auto mode and records the cluster in OCM.
resource "terraform_data" "rosa_hcp" {
  triggers_replace = [
    var.environment,
    var.openshift_version,
    join(",", module.vpc.private_subnets),
  ]
  provisioner "local-exec" {
    command = join(" ", compact([
      "rosa create cluster",
      "--cluster-name ${var.project}-${var.environment}",
      "--hosted-cp",
      "--region ${var.aws_region}",
      var.openshift_version != "" ? "--version ${var.openshift_version}" : "",
      "--subnet-ids ${join(",", module.vpc.private_subnets)}",
      "--replicas ${var.environment == "prod" ? 3 : 2}",
      var.private_cluster ? "--private" : "",
      "--mode auto --yes --watch",
    ]))
  }
  provisioner "local-exec" {
    when       = destroy
    command    = "rosa delete cluster --cluster ${self.input.cluster_name} --yes --watch"
    on_failure = continue
  }
  input = {
    cluster_name = "${var.project}-${var.environment}"
  }
}

locals {
  tags = {
    Project            = var.project
    Environment        = var.environment
    ManagedBy          = "Terraform"
    DataClassification = "Synthetic"
  }
}
