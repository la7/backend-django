output "env" {
  value       = var.env
  description = "Selected deployment environment."
}

output "s3_bucket_name" {
  value       = aws_s3_bucket.app_bucket.bucket
  description = "Name of the example S3 bucket created for this environment."
}
