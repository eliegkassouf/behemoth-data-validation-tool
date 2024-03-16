#!/usr/bin/env python3
# --------------------------------------------------------------
# Created By: Elie Kassouf
# Email: me@eliekassouf.ca
# Last Modified On: Saturday March 16th, 2024
# https://github.com/eliegkassouf/behemoth-data-validation-tool
# --------------------------------------------------------------
#
# WARNING/ATTENTION:
# Elie Kassouf assumes no responsibility for the use or
# reliability of this code.
#
# This code is presented "as is" without any guarantees.
# By using this code, you accept any and all risks.
#
# --------------------------------------------------------------
#
# This script is meant to serve as a starting point for your
# data validation needs and have not been tested yet. Please
# test this script in a development environment before using
# it in a production environment. This script is meant to
# change with your needs and should be modified to fit your
# specific use case.
#
# I used to perform pen testing and the easiest way to brute
# force is to use multiple instances because it's faster and
# harder to detect. So, I wrote this script to spin up multiple
# EC2 instances and assign a specific table to each instance
# for validation using the google-data-validation-tool.
#
# If you need more powerful instances, you can change the
# instance type to a more powerful one. Be aware that this will
# increase the cost of running the instances. Large instances
# can be expensive, so be sure to terminate the instances once
# the validation is complete to avoid unnecessary charges!
#
# This will ensure that the validation process is faster and
# more efficient, especially when dealing with a large number
# of tables.
#
# This should be able to handle validation for databases with
# 1TB or more of data. The google-data-validation-tool is a
# powerful tool that can handle large-scale data validation
# and provide detailed reports on the validation results.
#
# Notes:
# 1. Make sure to test the scripts in a development environment
#    before using them in a production environment.
# 2. Be sure to terminate the instances once the validation is
#    complete to avoid unnecessary charges.
# 3. The google-data-validation-tool is a powerful tool that can
#    handle large-scale data validation and provide detailed
#    reports on the validation results.
# 4. You can use CloudWatch to monitor the instances and set up
#    alarms to notify you when the validation is complete. This
#    will help you avoid unnecessary charges but will require
#    additional configuration from your end.
# 5. Replace YOUR_SOURCE_CONN, YOUR_TARGET_CONN, YOUR_SCHEMA,
#    and YOUR_TARGET_SCHEMA with your actual connection names
#    and schema.
# 6. The columns col1, col2, and col3 are placeholders for your
#    actual columns to validate.
# 7. The UserData script assumes Python3 and pip are available
#    in the AMI.
# --------------------------------------------------------------
#               Copyright © 2024 Elie G Kassouf
# --------------------------------------------------------------

import boto3


def create_instance(
    ec2_client,
    table_name,
    ami_id,
    instance_type,
    key_name,
    security_group_ids,
    subnet_id,
    iam_instance_profile_arn
):
 user_data_script = f"""#!/bin/bash
 sudo yum update -y
 sudo yum install git -y
 sudo yum install python3-pip -y
 git clone https://github.com/GoogleCloudPlatform/professional-services-data-validator.git
 cd professional-services-data-validator
 pip3 install -r requirements.txt
 pip3 install -e .
 python3 -m data_validation validate column --source-conn YOUR_SOURCE_CONN --target-conn YOUR_TARGET_CONN --tables-list YOUR_SCHEMA.{table_name}=YOUR_TARGET_SCHEMA.{table_name} --sum col1,col2 --count col3
 """
 instances = ec2_client.run_instances(
  ImageId=ami_id,
  InstanceType=instance_type,
  MinCount=1,
  MaxCount=1,
  KeyName=key_name,
  SecurityGroupIds=security_group_ids,
  SubnetId=subnet_id,
  UserData=user_data_script,
  TagSpecifications=[
   {
    'ResourceType': 'instance',
    'Tags': [
     {
      'Key': 'Name',
      'Value': f'ValidationInstance-{table_name}'
     },
    ]
   },
  ],
  IamInstanceProfile={
   'Arn': iam_instance_profile_arn
  }
 )
 return instances['Instances'][0]['InstanceId']


# Parameters for the EC2 instances
ami_id = 'AMI_ID'  # Replace with your AMI ID
instance_type = 't2.micro'  # Choose the instance type
key_name = 'YourKeyName'  # Replace with your key pair name
security_group_ids = ['sg-xxxxxxxx']  # Replace with your security group ID
subnet_id = 'subnet-xxxxxxx'  # Replace with your subnet ID
iam_instance_profile_arn = 'arn:aws:iam::123456789012:instance-profile/YourIAMRole'  # Replace with your IAM role ARN

# Define the number of instances and the specific table names to validate
num_instances = 5
table_names = ["table1", "table2", "table3", "table4", "table5"]  # Example table names

# Initialize a session using your credentials
session = boto3.Session(
 aws_access_key_id='YOUR_ACCESS_KEY',
 aws_secret_access_key='YOUR_SECRET_KEY',
 region_name='YOUR_REGION'
)

# Initialize the EC2 client
ec2 = session.client('ec2')

# Spin up instances and assign tables for validation
for i, table_name in enumerate(table_names):
 if i < num_instances:
  instance_id = create_instance(
   ec2,
   table_name,
   ami_id,
   instance_type,
   key_name,
   security_group_ids,
   subnet_id,
   iam_instance_profile_arn
  )
  print(f"Instance {instance_id} created for table {table_name}")