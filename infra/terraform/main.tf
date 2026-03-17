terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

variable "env" {
  type    = string
  default = "local"
  description = "Deployment environment name (local, dev, pro)."
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
  description = "AWS region to deploy resources into."
}

variable "aws_access_key" {
  type        = string
  default     = "test"
  description = "AWS access key (used by localstack in dev or by AWS credentials in pro)."
}

variable "aws_secret_key" {
  type        = string
  default     = "test"
  description = "AWS secret key (used by localstack in dev or by AWS credentials in pro)."
}

variable "localstack_endpoint" {
  type        = string
  default     = "http://localhost:4566"
  description = "LocalStack endpoint URL (only used in dev environment)."
}

locals {
  is_dev   = lower(var.env) == "dev"
  is_pro   = lower(var.env) == "pro"
  is_local = lower(var.env) == "local"
}

provider "aws" {
  region     = var.aws_region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key

  dynamic "endpoints" {
    for_each = local.is_dev ? [1] : []

    content {
      s3       = var.localstack_endpoint
      dynamodb = var.localstack_endpoint
    }
  }

  # Para LocalStack: usar estilo "path" en URLs de S3 (p.ej. http://localhost:4566/bucket)
  # El atributo correcto en el provider AWS v5+ es `s3_use_path_style`.
  s3_use_path_style = local.is_dev

  skip_credentials_validation = local.is_dev
  skip_metadata_api_check    = local.is_dev
  skip_requesting_account_id = local.is_dev
}

# Example resources (adjust/extend to match your real infra needs)
resource "aws_s3_bucket" "app_bucket" {
  bucket = "backend-django-${var.env}"

  tags = {
    Environment = var.env
    ManagedBy   = "terraform"
  }
}

resource "aws_s3_bucket_acl" "app_bucket_acl" {
  bucket = aws_s3_bucket.app_bucket.id
  acl    = "private"
}

resource "aws_dynamodb_table" "example" {
  count        = local.is_dev ? 1 : 0
  name         = "backend-django-${var.env}-table"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"

  attribute {
    name = "pk"
    type = "S"
  }

  tags = {
    Environment = var.env
    ManagedBy   = "terraform"
  }
}
