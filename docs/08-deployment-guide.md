# Deployment Guide

## Overview

The repository currently supports a deployment direction built around:

- Docker image
- ECS Fargate
- RDS PostgreSQL
- Secrets Manager
- Terraform

## Build The Image

```bash
docker build -t job-market-intelligence-platform .
```

## Infrastructure Provisioning

From the Terraform directory:

```bash
cd terraform
terraform init
terraform plan -var="aws_region=us-east-1"
terraform apply -var="aws_region=us-east-1"
```

## Required Inputs

At minimum, configure:

- AWS region
- container image URI
- database password
- environment name

See [terraform/terraform.tfvars.example](../terraform/terraform.tfvars.example).

## Deployment Flow

1. Build and publish the container image.
2. Provision or update Terraform-managed infrastructure.
3. Update ECS task definition with the image URI.
4. Allow the application container to read the database secret.
5. Run migrations on startup.
6. Verify `GET /health`, `GET /ready`, and `GET /metrics`.

## Post-Deploy Validation

- confirm ALB responds successfully
- confirm ECS task reaches steady state
- confirm database connectivity
- upload a sample job
- run a sample candidate match request

## Current Limitations

- no blue/green deployment strategy yet
- no Terraform remote-state backend is configured yet
- no production secret rotation workflow yet
- no external tracing or alert platform is configured yet
