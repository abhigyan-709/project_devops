resource "aws_instance" "ec2-master-cluster" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t2.medium"
  key_name               = aws_key_pair.mongo_key.key_name
  security_groups        = [aws_security_group.mongo_security_group.name]
  iam_instance_profile   = aws_iam_instance_profile.admin_profile.name

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

    # Initialize the Kubernetes master node
    sudo kubeadm init --pod-network-cidr=10.244.0.0/16

    # Set up kubeconfig for the ubuntu user
    mkdir -p $HOME/.kube
    sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
    sudo chown $(id -u):$(id -g) $HOME/.kube/config

    # Install Flannel CNI plugin
    kubectl apply -f https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml
  EOF

  tags = {
    Name        = "K8-Master-EC2"
    Environment = "Development"
    Project     = "KubernetesCluster"
  }
}
