resource "aws_s3_bucket" "terraform_state_bucket" {
  bucket = "project-devops-state-bucket"  # Change this to a globally unique name            
}

resource "aws_s3_bucket_ownership_controls" "terraform_state_bucket_ownership" {
  bucket = aws_s3_bucket.terraform_state_bucket.id

  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "terraform_state_bucket_acl" {
  depends_on = [aws_s3_bucket_ownership_controls.terraform_state_bucket_ownership]

  bucket = aws_s3_bucket.terraform_state_bucket.id
  acl    = "private"
}
