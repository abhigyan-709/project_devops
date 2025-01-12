resource "aws_instance" "mongo_instance" {
  ami           = "ami-053b12d3152c0cc71"  # Update with the latest Ubuntu AMI ID
  instance_type = "t2.micro"               # Choose your instance type
  key_name      = aws_key_pair.mongo_key.key_name
  security_groups = [aws_security_group.mongo_security_group.name]
  iam_instance_profile = aws_iam_instance_profile.admin_profile.name

  root_block_device {
    volume_size = 20 # Increase root volume size to 20 GB
    volume_type = "standard" # Use General Purpose SSD (gp2) for better performance
  }

  tags = {
    Name = "MongoDB-EC2"
  }
}
