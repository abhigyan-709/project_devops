pipeline {
    agent any

    environment {
        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')
        MONGO_URI = credentials('MONGO_URI')
        EC2_SSH_KEY = credentials('EC2_SSH_KEY')
        AWS_REGION = 'ap-south-1'
        ECR_REGISTRY = '774305585645.dkr.ecr.ap-south-1.amazonaws.com'
        ECR_REPO = 'project-devops'
        K8S_MASTER_IP = 'ec2-13-201-126-178.ap-south-1.compute.amazonaws.com'
        K8S_WORKER_IP = 'ec2-65-1-111-131.ap-south-1.compute.amazonaws.com'
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Set up AWS credentials') {
            steps {
                script {
                    withAWS(credentials: ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY'], region: AWS_REGION) {
                        // AWS credentials are automatically configured
                    }
                }
            }
        }

        stage('Install Terraform') {
            steps {
                sh 'curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -'
                sh 'sudo apt-add-repository "deb https://apt.releases.hashicorp.com $(lsb_release -cs) main"'
                sh 'sudo apt-get update && sudo apt-get install terraform=1.5.6'
            }
        }

        stage('Terraform Init') {
            steps {
                dir('infrastructure') {
                    sh 'terraform init -backend-config="bucket=project-devops-state-bucket" -backend-config="key=terraform.tfstate" -backend-config="region=ap-south-1"'
                }
            }
        }

        stage('Terraform Plan') {
            steps {
                dir('infrastructure') {
                    sh 'terraform plan'
                }
            }
        }

        stage('Terraform Apply') {
            steps {
                dir('infrastructure') {
                    sh 'terraform apply -auto-approve'
                }
            }
        }

        stage('Install Docker Compose') {
            steps {
                sh '''
                    sudo apt-get update
                    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
                    sudo chmod +x /usr/local/bin/docker-compose
                    docker-compose --version
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build --build-arg MONGO_URI=${MONGO_URI} -t project-devops -f ./app/Dockerfile ./app'
            }
        }

        stage('Log in to Amazon ECR') {
            steps {
                withAWS(credentials: ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY'], region: AWS_REGION) {
                    sh 'aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY'
                }
            }
        }

        stage('Tag Docker Image') {
            steps {
                sh 'docker tag project-devops:latest $ECR_REGISTRY/$ECR_REPO:latest'
            }
        }

        stage('Push Docker Image to ECR') {
            steps {
                sh 'docker push $ECR_REGISTRY/$ECR_REPO:latest'
            }
        }

        stage('Set up SSH key for EC2') {
            steps {
                writeFile file: 'ec2-key.pem', text: "${EC2_SSH_KEY}"
                sh 'chmod 600 ec2-key.pem'
            }
        }

        stage('Retrieve kubeconfig from EC2 Master') {
            steps {
                script {
                    sh """
                        ssh -o StrictHostKeyChecking=no -i ec2-key.pem ubuntu@$K8S_MASTER_IP "sudo cat /etc/kubernetes/admin.conf" > kubeconfig
                        sed -i 's/172.31.41.132/$K8S_MASTER_IP/' kubeconfig
                        export KUBECONFIG=kubeconfig
                        kubectl get nodes --insecure-skip-tls-verify
                    """
                }
            }
        }

        stage('Copy Kubernetes deployment files to EC2 Worker Node') {
            steps {
                script {
                    sh """
                        scp -o StrictHostKeyChecking=no -i ec2-key.pem ./k8-deployments/deployment.yaml ubuntu@$K8S_WORKER_IP:/home/ubuntu/k8-deployments/
                        scp -o StrictHostKeyChecking=no -i ec2-key.pem ./k8-deployments/services.yaml ubuntu@$K8S_WORKER_IP:/home/ubuntu/k8-deployments/
                    """
                }
            }
        }

        stage('Install AWS CLI on Worker Node') {
            steps {
                script {
                    sh """
                        ssh -o StrictHostKeyChecking=no -i ec2-key.pem ubuntu@$K8S_WORKER_IP << 'EOF'
                            sudo apt-get update
                            sudo apt-get install -y awscli
                            aws --version
                        EOF
                    """
                }
            }
        }

        stage('Create ECR Secret on Worker Node') {
            steps {
                script {
                    sh """
                        ssh -o StrictHostKeyChecking=no -i ec2-key.pem ubuntu@$K8S_WORKER_IP \
                            "kubectl delete secret ecr-secret --ignore-not-found && \
                            aws ecr get-login-password --region $AWS_REGION | \
                            kubectl create secret docker-registry ecr-secret \
                            --docker-server=$ECR_REGISTRY \
                            --docker-username=AWS \
                            --docker-password=\$(cat) \
                            --docker-email=your-email@example.com"
                    """
                }
            }
        }

        stage('Deploy to Kubernetes on EC2') {
            steps {
                script {
                    sh """
                        ssh -o StrictHostKeyChecking=no -i ec2-key.pem ubuntu@$K8S_WORKER_IP << 'EOF'
                            kubectl apply -f ./k8-deployments/deployment.yaml
                            kubectl apply -f ./k8-deployments/services.yaml
                        EOF
                    """
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
