output "cluster_name" {
  value = terraform_data.rosa_hcp.output.cluster_name
}
output "ecr_repositories" {
  value = { for k, v in aws_ecr_repository.services : k => v.repository_url }
}
output "opensearch_endpoint" {
  value = aws_opensearch_domain.logs.endpoint
}
output "audit_bucket" {
  value = aws_s3_bucket.audit.id
}
output "kms_key_arn" {
  value = aws_kms_key.platform.arn
}
