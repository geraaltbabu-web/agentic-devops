variable "aws_region" {
  type    = string
  default = "us-east-1"
}
variable "environment" {
  type    = string
  default = "dev"
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "environment must be dev, staging, or prod."
  }
}
variable "project" {
  type    = string
  default = "banking-demo"
}
variable "vpc_cidr" {
  type    = string
  default = "10.40.0.0/16"
}
variable "private_cluster" {
  type    = bool
  default = false
}
variable "openshift_version" {
  type    = string
  default = ""
  description = "Optional ROSA version. Empty selects the current supported default."
}
variable "services" {
  type    = list(string)
  default = ["accounts", "payments", "ledger", "fraud", "notifications"]
}
