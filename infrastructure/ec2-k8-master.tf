# Fetch the latest Ubuntu AMI
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]  # Canonical
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
}

# Key pair for SSH access
resource "aws_key_pair" "mongo_key" {
  key_name   = "k8s-cluster-key"
  public_key = file("~/.ssh/id_rsa.pub")  # Path to your public SSH key
}

# Security group for Kubernetes master node
resource "aws_security_group" "mongo_security_group" {
  name_prefix = "k8s-master-sg"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Allow SSH from anywhere
  }

  ingress {
    from_port   = 6443
    to_port     = 6443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Kubernetes API server
  }

  ingress {
    from_port   = 10250
    to_port     = 10250
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Kubelet API
  }

  ingress {
    from_port   = 8472
    to_port     = 8472
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]  # Flannel overlay network
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# IAM instance profile for administrative access
resource "aws_iam_role" "admin_role" {
  name = "k8s-master-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_instance_profile" "admin_profile" {
  name = "k8s-master-profile"
  role = aws_iam_role.admin_role.name
}

# Kubernetes master node EC2 instance
resource "aws_instance" "ec2-master-cluster" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t2.medium"
  key_name               = aws_key_pair.mongo_key.key_name
  security_groups        = [aws_security_group.mongo_security_group.name]
  iam_instance_profile   = aws_iam_instance_profile.admin_profile.name

  user_data = <<-EOF
      #!/bin/bash
      set -e
      sudo apt update
      sudo apt install -y apt-transport-https ca-certificates curl
      curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
      cat <<EOF2 | sudo tee /etc/apt/sources.list.d/kubernetes.list
      deb https://apt.kubernetes.io/ kubernetes-xenial main
      EOF2
      sudo apt update
      sudo apt install -y kubelet kubeadm kubectl
      sudo apt-mark hold kubelet kubeadm kubectl
      sudo kubeadm init --pod-network-cidr=10.244.0.0/16
      mkdir -p $HOME/.kube
      sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
      sudo chown $(id -u):$(id -g) $HOME/.kube/config
      kubectl apply -f https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml
  EOF

  tags = {
    Name        = "K8-Master-EC2"
    Environment = "Development"
    Project     = "KubernetesCluster"
  }
}

# Output variables
output "instance_id" {
  description = "The ID of the Kubernetes master EC2 instance"
  value       = aws_instance.ec2-master-cluster.id
}

output "public_ip" {
  description = "The public IP address of the Kubernetes master EC2 instance"
  value       = aws_instance.ec2-master-cluster.public_ip
}

output "kubeconfig" {
  description = "The kubeconfig file for connecting to the Kubernetes cluster"
  value       = <<-EOF
    apiVersion: v1
    clusters:
    - cluster:
        certificate-authority-data: <DATA_OMITTED>
        server: https://${aws_instance.ec2-master-cluster.public_ip}:6443
      name: kubernetes
    contexts:
    - context:
        cluster: kubernetes
        user: admin
      name: kubernetes
    current-context: kubernetes
    kind: Config
    preferences: {}
    users:
    - name: admin
      user:
        client-certificate-data: <DATA_OMITTED>
        client-key-data: <DATA_OMITTED>
  EOF
}
