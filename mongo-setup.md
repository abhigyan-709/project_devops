# Login to your AWS EC2 instance via ssh in your terminal 

## AWS EC2 ssh command 

```bash
# change you working directory or get into the directory where your ssh key is located

chmod 400 "path/to/key/you-ssh-key-name.pem"
ssh -i "your-key-name.pem" ubuntu@ec2-public-ip-of-ec2.ap-south-1.compute.amazonaws.com

# if you are login for the first time then it will ask you add the fingerprint of this instance in your computer, type yes

# import the public key
sudo apt-get install gnupg curl 

# curl the gpg key for the mongoDB 
curl -fsSL https://www.mongodb.org/static/pgp/server-8.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-8.0.gpg \
   --dearmor

# create a list file for the mongoDB 
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


# here you have installed the MongoDB database in your EC2 instance, now we will configure it for out database uses
# please note that the below mentioned practice is not suggested for your production enviroment, you will have to use string authentication and RBAC techniquies for production environments.

# in the same instance connect to the mongo-db shell
mongosh

# switch to admin database
use admin 

# use the following command to add an admin user with your desired password
db.createUser({user: "admin", pwd: "Gyanu1234", roles: [{ role: "root", db: "admin" }]})

# you can also update your user by using below command 
db.updateUser("admin", {pwd: "Gyanu1234", roles: [{ role: "root", db: "admin" }]})

# exit the mongodb shell 
exit

# now we will enable the mongodb authentication by adding some changes in the mongodb config file 

# open the mongodb config file 
sudo nano /etc/mongod.conf

# add the following code or replace with the previous added code, only change thes blocks, and leave the rest of the congiguration as it is.

security:
     authorization: "enabled"

# change the bindip from 127.0.0.1 to 0.0.0.0
net:
    port: 27017
    bindIp: 0.0.0.0  # Allow connections from any IP


# save and exit the configuration 
# restart the mongodb servcice to perform the changes 
sudo systemctl restart mongod 


```

## You can use mongoDB compass to get connected with your live mongodb database by using the below URI.

```bash
MONGO_URI=mongodb://admin:your_secure_password@3.108.51.102:27017/?authSource=admin
```
