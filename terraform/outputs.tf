output "ec2_public_ip" {
  description = "Public EC2 IP Address"
  value       = aws_instance.tg_ec2.public_ip
}

output "ecr_repository_url" {
  description = "ECR Repository URL"
  value       = aws_ecr_repository.tg_ecr_repo.repository_url
}
