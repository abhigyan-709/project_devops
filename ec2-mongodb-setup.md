# How to install mongodb in AWS EC2 Ubuntu Instance

```bash 
# assuming you have seen how to setup the ec2-mongodb-setup.md
# login to your ec2 instance via ssh
# prepare the .pem key, if you have setup the AWS EC2 instance via terraform 
infrastructure/terraform output private_key
# paste the key in mongo-db.pem file
# ssh into your ubuntu instance 
# run chmod
 chmod 400 "mongo-key.pem"
 ssh -i "mongo-key.pem" ubuntu@ec2-public-ip-of-ec2.ap-south-1.compute.amazonaws.com # replace public ip of ec2 like 0-01-02-012
 ssh -i "mongo-key.pem" ubuntu@ec2-3-108-51-102.ap-south-1.compute.amazonaws.com # for example

 # import public key
 sudo apt-get install gnupg curl

 # curl the gpg key for mongodb
 curl -fsSL https://www.mongodb.org/static/pgp/server-8.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-8.0.gpg \
   --dearmor
 # create the list file
 echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] https://repo.mongodb.org/apt/ubuntu noble/mongodb-org/8.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list

 # reload the local package database
 sudo apt-get update

 # install the stable version of the mongodb
 sudo apt-get install -y mongodb-org

 # start the mongod service
 sudo systemctl start mongod
 
 # if service not found, run the deamon once again 
 sudo systemctl daemon-reload

 # verify the mongodb started successfully
 sudo systemctl status mongod

 # if you want mongodb to be re-start when the system is booted
 sudo systemctl enable mongod

```