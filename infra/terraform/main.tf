# This is a demonstration of Infrastructure as Code (IaC) for the RAG project.
# In a real scenario, this would provision resources like AWS ECS, S3, or RDS.

provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "document_storage" {
  bucket = "enterprise-rag-documents"
  acl    = "private"

  tags = {
    Name        = "RAG Document Store"
    Environment = "Production"
  }
}

resource "aws_ecr_repository" "app_repo" {
  name                 = "enterprise-rag-ops"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}
