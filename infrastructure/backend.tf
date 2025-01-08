terraform {
  backend "s3" {
    bucket = "project-devops-state-bucket"  # Must match the S3 bucket name
    key    = "terraform.tfstate"
    region = "ap-south-1"  # Change to your desired region
  }
}
