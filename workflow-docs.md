# GitHub Actions Workflow Documentation: Docker Build, Push to AWS ECR & Terraform Setup

## Overview
This GitHub Actions workflow automates the CI/CD process for a project. It includes the following tasks:
1. Building a Docker image for the application.
2. Pushing the Docker image to AWS Elastic Container Registry (ECR).
3. Setting up and deploying infrastructure using Terraform.
4. Deploying the application to a Kubernetes cluster running on EC2 instances.

The workflow is triggered on a `push` event to the `main` branch of the repository.

---

## Workflow Structure

### **Trigger**
- The workflow runs on a `push` event to the `main` branch.

---

### **Jobs**

#### 1. **Build Job**
This job performs the following tasks:
- **Checkout Code**: Retrieves the code from the repository.
- **Set Up AWS Credentials**: Configures AWS credentials using secrets stored in GitHub.
- **Install Terraform**: Installs a specific version of Terraform.
- **Terraform Init and Plan**:
  - Initializes Terraform with backend configuration.
  - Plans infrastructure changes.
- **Terraform Apply**: Applies the planned Terraform changes to set up infrastructure.
- **Install Docker Compose**: Installs Docker Compose on the runner.
- **Build Docker Image**:
  - Builds the Docker image with the `MONGO_URI` build argument.
- **Log In to Amazon ECR**: Logs into the private AWS ECR registry.
- **Tag Docker Image**: Tags the Docker image for ECR.
- **Push Docker Image to ECR**: Pushes the tagged image to the ECR repository.

#### 2. **Deploy Job**
This job performs the following tasks:
- **Checkout Code**: Retrieves the code from the repository.
- **Set Up SSH Key for EC2**:
  - Configures SSH access to EC2 instances using a private key stored in GitHub secrets.
- **Retrieve Kubeconfig from EC2 Master Node**:
  - Retrieves the Kubernetes configuration file from the EC2 master node.
  - Updates the configuration file to use the public IP address.
  - Exports the `KUBECONFIG` environment variable.
  - Validates Kubernetes connectivity by listing nodes.
- **Copy Kubernetes Deployment Files to EC2 Worker Node**:
  - Transfers deployment and service YAML files to the EC2 worker node.
- **Install AWS CLI on Worker Node**:
  - Installs AWS CLI on the worker node to manage AWS resources.
- **Create ECR Secret on Worker Node**:
  - Deletes any existing ECR secret and creates a new one using the AWS ECR login credentials.
- **Deploy to Kubernetes on EC2**:
  - Deploys the application to the Kubernetes cluster by applying deployment and service YAML files.

---

## Key Features

### **AWS Integration**
- The workflow uses AWS services for:
  - Storing Docker images in ECR.
  - Managing infrastructure with Terraform.
  - Deploying the application to an EC2-hosted Kubernetes cluster.

### **Terraform Setup**
- Initializes Terraform with a backend configuration.
- Plans and applies changes to manage infrastructure.

### **Docker Workflow**
- Builds and tags a Docker image.
- Pushes the image to AWS ECR for containerized deployments.

### **Kubernetes Deployment**
- Uses Kubernetes on EC2 instances for deploying and managing the application.
- Handles ECR image authentication using Kubernetes secrets.

---

## Secrets Used
- `AWS_ACCESS_KEY_ID`: AWS Access Key for authentication.
- `AWS_SECRET_ACCESS_KEY`: AWS Secret Key for authentication.
- `MONGO_URI`: MongoDB connection string for the application.
- `EC2_SSH_KEY`: Private SSH key for accessing EC2 instances.

---

## Notes
- Ensure all required secrets are securely stored in the repository settings under `Settings > Secrets and variables > Actions`.
- Update the ECR repository URL and EC2 instance details as per your setup.
- Use the appropriate region (`ap-south-1` in this case) for all AWS-related configurations.

---

## Workflow Trigger
- The workflow is triggered automatically when a push is made to the `main` branch.

---

## Benefits
- Automates the CI/CD pipeline for efficient application deployment.
- Ensures consistency in infrastructure setup using Terraform.
- Simplifies Kubernetes deployments on EC2 instances.
