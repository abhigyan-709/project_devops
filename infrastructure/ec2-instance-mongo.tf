resource "aws_instance" "mongo_instance" {
  ami           = "ami-053b12d3152c0cc71"  # Update with the latest Ubuntu AMI ID
  instance_type = "t2.micro"               # Choose your instance type
  key_name      = aws_key_pair.mongo_key.key_name
  security_groups = [aws_security_group.mongo_security_group.name]
  iam_instance_profile = aws_iam_instance_profile.admin_profile.name

  user_data = <<-EOF
    #!/bin/bash
    apt update
    apt install -y mongodb
    systemctl start mongodb
    systemctl enable mongodb
  EOF

  tags = {
    Name = "MongoDB-EC2"
  }
}
