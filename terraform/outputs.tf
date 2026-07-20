output "alb_dns_name" {
  description = "DNS name of the application load balancer."
  value       = aws_lb.api.dns_name
}

output "ecs_cluster_name" {
  description = "Name of the ECS cluster."
  value       = aws_ecs_cluster.main.name
}

output "ecs_service_name" {
  description = "Name of the ECS service."
  value       = aws_ecs_service.api.name
}

output "database_endpoint" {
  description = "RDS PostgreSQL endpoint."
  value       = aws_db_instance.postgres.address
}

output "database_secret_arn" {
  description = "ARN of the database URL secret."
  value       = aws_secretsmanager_secret.database_url.arn
}
