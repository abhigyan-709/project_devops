data "aws_ami" "ubuntu" {
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
