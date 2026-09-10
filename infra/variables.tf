variable "aws_region" {
  description = "AWS region for all resources. Route 53 and IAM are global; S3/CloudFront/ACM must be us-east-1 for CloudFront to use the cert."
  type        = string
  default     = "us-east-1"
}

variable "domain_name" {
  description = "Domain served by this stack (a subdomain, delegated from the acciondatalabs.com Cloudflare zone via an NS record)."
  type        = string
  default     = "aiexplorer.acciondatalabs.com"
}

variable "github_repo" {
  description = "GitHub org/repo allowed to assume the deploy role via OIDC."
  type        = string
  default     = "yadavilli-solutions/yadavilli.com"
}

variable "github_branch" {
  description = "Branch allowed to assume the deploy role via OIDC."
  type        = string
  default     = "main"
}
