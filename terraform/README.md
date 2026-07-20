# Terraform

This directory contains the initial AWS infrastructure baseline for the Job Market Intelligence Platform.

## Scope

The current baseline provisions:

- VPC with public and private subnets
- Internet Gateway and route tables
- Security groups
- ECS cluster
- ECS Fargate service for the FastAPI application
- Application Load Balancer
- RDS PostgreSQL instance
- Secrets Manager secret for the database URL
- CloudWatch log group
- IAM roles for ECS task execution and application runtime

## Intended Usage

This baseline is intended for development and evaluation environments. It has not yet been hardened for multi-environment production use.

Follow-on phases should expand:

- environment separation
- state backend strategy
- parameterization of sizing
- monitoring and alerting
- secret rotation

## Example Workflow

```bash
cd terraform
terraform init
terraform plan -var="aws_region=us-east-1"
terraform apply -var="aws_region=us-east-1"
```
