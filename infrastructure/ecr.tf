# Define the AWS provider
provider "aws" {
  region = "ap-south-1" # Replace with your desired region
}

# Create the ECR repository
resource "aws_ecr_repository" "docker_repo" {
  name = "project-devops" # Replace with your desired repository name
}

# Output the ECR repository URL
output "ecr_repository_url" {
  value       = aws_ecr_repository.docker_repo.repository_url
  description = "The URL of the ECR repository"
}
