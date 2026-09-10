output "bucket_name" {
  value = aws_s3_bucket.site.bucket
}

output "cloudfront_distribution_id" {
  value = aws_cloudfront_distribution.site.id
}

output "cloudfront_domain_name" {
  value = aws_cloudfront_distribution.site.domain_name
}

output "deploy_role_arn" {
  value = aws_iam_role.deploy.arn
}

output "route53_name_servers" {
  description = "Point acciondatalabs.com's registrar at these nameservers to make Route 53 authoritative."
  value       = aws_route53_zone.site.name_servers
}
