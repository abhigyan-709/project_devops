# This repository uses below technoligies to illustrate practical DevOps Practice

1. Python as base programming language
2. FastAPI for the RestAPI development (this is python based restapi web framework)
3. Docker to bind the Application in image 
4. Kubernetes for Container Orchestration, deployment, replicaset devlopment [we will deploy the API in 3 replicaset]
5. MongoDB for storage of the data, recieved through API CRUD operation 
6. AWS EC2, ECR, EKS, S3, IAM, Cloudwatch & other required managed services
7. Terraform for infrastructure provisioning & management 
8. GitHub Actions for CI-CD pipelines 

## Setup Commands and Manual Operations of FastAPI

### 1. Activate the virtual environment
```bash 
# considering the mac system as the code is developed in mac environment
python3 -m venv venv
# activate the virtual environment
source ./venv/bin/activate
```

### 2. Clone the Code
```bash 
# use the below link to clone the file in your local environment
git clone git@github.com:abhigyan-709/project_devops.git
```

### 3. Test the code locally by preparing the Docker Image
```bash 
# two ways to run the code, either just prepare the docker image [preferred way]
# use the directory /your-project/project-devops/app/Dockerfile or just make sure you are in dockerfile location
# if you have mongodb connection then you can run this app by providing the mongodb uri

# see the mongodb-setup.md file to know how the mongodb is cofigured
# FastAPI in local docker container, with live database 
docker build -t project-devops .
docker run -d -p 8000:8000 project-devops
```

> project-devops is the tag name for the image I have used, you can use any of your desired name
> Docker Deamon should be running in your local system, if its not available please use official docker website to download it

### 4. Test the working of API with AWS or Locally with docker-compose
```bash 
# run the app with docker-compose with live or containerised mongodb in your local system
# if you are intended to run the application in the multicontainer 
# to run locally replace .env mongodb uri with mongodb://localhost:27017 or just enter the live database URI of mongodb

root-dir/docker-compose build
root-dir/docker-compose up -d #-d is for deatching the container from the terminal

```

Here I am using AWS EC2 Instance for MongoDB database storage, you can also add docker-compose.yaml service, or in this same project i am demonstrating this.

### 5. Setup the AWS CLI and Configure the AWS ID | Assuming you already have AWS Free Tier Limit Account
```bash 
# get the AWS ACCESS ID & Secret by creating manually via AWS console in AWS IAM indentity center.
# be cautious to not to store the root ID in AWS CLI, for test purpose i have done so, and I have already reset those keys
aws configure
AWS Access Key ID [**********]:
AWS Secret Access Key [***********]:
Default region name [ap-south-1] # my region is ap-south-1(mumbai) change it accordingly
Default output format [None]: # json or txt
```
### 6. Provision the infrastructure with terraform

```bash 
# assuming you have seen how to setup the terrafrom in your local device first
infrastructure/terraform init
infrastructure/terraform plan
infrastructure/terraform apply
```

### 7. Connect the ec2 instance to prepare the mongodb in ubuntu instance with authentication mode
```bash 
# assuming you have seen how to setup the ec2-mongodb-setup.md


```
