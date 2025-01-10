# Data source for the latest Ubuntu AMI
data "aws_ami" "ubuntu_worker" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical's AWS Account ID
}

# Define IAM role for Kubernetes Worker (with Admin access)
resource "aws_iam_role" "k8s_worker_role" {
  name = "k8s-worker-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

# Attach Admin policy to Kubernetes Worker IAM role
resource "aws_iam_role_policy_attachment" "k8s_worker_admin_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
  role       = aws_iam_role.k8s_worker_role.name
}

# Define IAM instance profile for Kubernetes Worker
resource "aws_iam_instance_profile" "k8s_worker_instance_profile" {
  name = "k8s-worker-instance-profile"
  role = aws_iam_role.k8s_worker_role.name
}

# Define Security Group for Kubernetes Worker EC2 instance
resource "aws_security_group" "k8s_worker_security_group" {
  name        = "k8s-worker-security-group"
  description = "Allow Kubernetes access"

  ingress {
    from_port   = 6443
    to_port     = 6443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 2379
    to_port     = 2380
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 10250
    to_port     = 10250
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 10259
    to_port     = 10259
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 10257
    to_port     = 10257
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # For Flannel VXLAN network communication
  ingress {
    from_port   = 8472
    to_port     = 8472
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # NodePort services
  ingress {
    from_port   = 30000
    to_port     = 32767
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Egress rules (allow all outbound traffic)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 instance for Kubernetes Worker node
resource "aws_instance" "ec2_worker_cluster" {
  ami                    = data.aws_ami.ubuntu_worker.id
  instance_type          = "t2.micro"
  key_name               = aws_key_pair.mongo_key.key_name
  security_groups        = [aws_security_group.k8s_worker_security_group.name]
  iam_instance_profile   = aws_iam_instance_profile.k8s_worker_instance_profile.name

  tags = {
    Name        = "K8-Worker-EC2"
    Environment = "Development"
    Project     = "KubernetesCluster"
  }
}
