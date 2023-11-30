# Microservice_Application_with_MongoDBAtlas_AWSCDK_APIGW_Lambda
This is a reference architecture for API based application with MongoDB Atlas , APIGW and Lambda

## [MongoDB Atlas](https://www.mongodb.com/atlas) 
MongoDB Atlas is an all purpose database having features like Document Model, Geo-spatial , Time-seires, hybrid deployment, multi cloud services.
It evolved as "Developer Data Platform", intended to reduce the developers workload on development and management the database environment.
It also provide a free tier to test out the application / database features.

## [Amazon API Gateway](https://aws.amazon.com/api-gateway/)

Amazon API Gateway is a fully managed service that makes it easy for developers to create, publish, maintain, monitor, and secure APIs at any scale.

## [Amazon Cognito User pool](https://aws.amazon.com/pm/cognito)

Amazon Cognito User pool helps you to deliver frictionless customer identity and access management (CIAM) with a cost-effective and customizable platform. Helps you to add security features such as adaptive authentication, support compliance, and data residency requirements.It can scale to millions of users across devices with a fully managed, high-performant, and reliable identity store.
#


1.## Prerequisites

This demo, instructions, scripts and cloudformation template is designed to be run in `us-east-1`. With few modifications you can try it out in other regions as well. Make sure to change REGION_NAME in global_args.py if not using US-EAST-1
    
        -  AWS CLI Installed & Configured 
        -  AWS CDK Installed & Configured
        -  MongoDB Atlas Account 
        -  Python Packages :
          - Python3 - `yum install -y python3`
          - Python Pip - `yum install -y python-pip`
          - Virtualenv - `pip3 install virtualenv`

2.## Setting up the environment

Get the application code

git clone https://github.com/mongodb-partners/Microservice_Application_with_MongoDBAtlas_AWSCDK_APIGW_Lambda.git
cd aws_mongodb_sample_dir


3.## Prepare the dev environment to run AWS CDK

We will use `cdk` to make our deployments easier. Lets go ahead and install the necessary components.

# You should have npm pre-installed
# If you DONT have cdk installed
npm install -g aws-cdk

# Make sure you in root directory
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt

cd aws_mongodb_sample
pip install --target ./dependencies pymongo
cd ..

# Set Environment Variables
    export ORG_ID="<ORG_ID>"
    export MONGODB_USER="<MONGODB_USER>"
    export MONGODB_PASSWORD="<MONGODB_PASSWORD>"

cdk bootstrap aws://<ACCOUNT_NUMBER>/<AWS-REGION> 

cdk ls
# Follow on screen prompts

You should see an output of the available stacks,

aws_mongo_db_create
aws_mongodb_sample_stack

4.##  Deploying the application

Let us walk through each of the stacks,

 **Stack: aws_mongo_db_create**

This stack will create four resources and return Mongo Db Atlas URL 
    a)	MongoDB::Atlas::Cluster
    b)	MongoDB::Atlas::Project
    c)	MongoDB::Atlas::DatabaseUser
    d)	MongoDB::Atlas::ProjectIpAccessList

**Stack: aws_mongodb_sample_stack**

This stack will create 
      a)	Secret for storing ATLAS DB URI
      b)	Cognito User Pool for API Authentication
      c)	Lambda function that will create a datbase and insert dummy data and return document count
      d)	API Gateway backed by the lambda function created above

cdk deploy --all

After successfully deploying the stack, Check the `Outputs` section of the stack aws_mongodb_sample_stack, you will see ApiGatewayEndpoint created.


## **Clean up**

Use `cdk destroy --all` to clean up all the AWS CDK resources. 
Terminate the MongoDB Atlas cluster.

## Troubleshooting

Refer [this link](https://github.com/mongodb/mongodbatlas-cloudformation-resources/tree/master#troubleshooting) to resolve some common issues encountered when using AWS CloudFormation/CDK with MongoDB Atlas Resources.



## Useful commands
 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
