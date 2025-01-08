# This repository uses below technoligies to illustrate practical DevOps Practice

# Technology Stack

- ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
- ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
- ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
- ![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
- ![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
- ![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
- ![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)
- ![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) 
- ![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
- ![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)

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

# ssh into your EC2 instance 
ssh -i "mongo-key.pem" ubuntu@3.108.51.102

# connect to mongodb 
mongosh

# switch to admin database 
use admin 

# add the follwing command to add user as admin with desired password

db.createUser({
  user: "admin",
  pwd: "your_secure_password",  # Replace with a strong password
  roles: [{ role: "root", db: "admin" }]
})

# exit the shell
exit

```

> Enable the other settings
>
> ```bash
> # Enable Authentication in MongoDB Configuration
> # open the mongodb config file
> sudo nano /etc/mongod.conf
>   security:
>     authorization: "enabled"
> # change the bindip from 127.0.0.1 to 0.0.0.0
>   net:
>     port: 27017
>     bindIp: 0.0.0.0  # Allow connections from any IP
>
> # save and exit 
> sudo systemctl restart mongod # restart the mongodb service
> ```
> 

```bash 
# edit the .env for custom mongodb uri
MONGO_URI=mongodb://admin:your_secure_password@3.108.51.102:27017/?authSource=admin

# restart the container after changing the docker-compose file 
environment: 
       - .env # MongoDB URI for the FastAPI app

    
```

### 8. restart the docker-conatiners with new mongodb URI changes

### 9. Pushing the prepared docker image to the contaner registry : AWS ECR