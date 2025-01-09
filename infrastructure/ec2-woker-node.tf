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

  user_data = <<-EOF
    #!/bin/bash
    set -e
    # Update and install dependencies
    sudo apt update
    sudo apt install -y apt-transport-https ca-certificates curl

    # Add Kubernetes repository and install Kubernetes components
    curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
    sudo tee /etc/apt/sources.list.d/kubernetes.list <<EOF2
    deb https://apt.kubernetes.io/ kubernetes-xenial main
    EOF2
    sudo apt update
    sudo apt install -y kubelet kubeadm kubectl
    sudo apt-mark hold kubelet kubeadm kubectl

    # Join the Kubernetes cluster using the kubeadm join command
    sudo kubeadm join 172.31.39.63:6443 --token aft43k.dar590homwoev6sq --discovery-token-ca-cert-hash sha256:ecbef09d9ffe7d4acfcc959623a977619d0c0b3524049cf55024c274bbf2c8fa
  EOF

  tags = {
    Name        = "K8-Worker-EC2"
    Environment = "Development"
    Project     = "KubernetesCluster"
  }
}
