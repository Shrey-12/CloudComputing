import boto3
from time import sleep

Endpoint = None

def create_instance(startup_script):
    try:
        ec2 = boto3.client('ec2', region_name='ap-south-1')
        reservation = ec2.run_instances(
            ImageId='ami-0da59f1af71ea4ad2',
            MaxCount=1,
            MinCount=1,
            InstanceType='t2.micro',
            KeyName='cc-kp',
            SecurityGroups=['launch-wizard-1'],
            UserData=startup_script,
            IamInstanceProfile={
                 'Arn': 'arn:aws:iam::677027043458:instance-profile/ec2_s3'
            }
        )
        return reservation
        
        
    except Exception as e:
        print(e)

def create_rds_instance():
    rds = boto3.client('rds')
    res=None
    try:
        res = rds.describe_db_instances(
            DBInstanceIdentifier="shreydbid"
        )
    finally:

        if res == None:
            rds.create_db_instance(
            DBInstanceClass="db.t3.micro",
            Engine="mariadb",
            DBInstanceIdentifier = "shreydbid",
            MasterUsername="user",
            MasterUserPassword="user1234",
            AllocatedStorage=10,
            VpcSecurityGroupIds = [
                'sg-00353d980f9c8b910'
            ],
            AvailabilityZone="ap-south-1a"
            )
        res = rds.describe_db_instances(
        DBInstanceIdentifier='shreydbid'
    )
        print(res['DBInstances'][0]['DBInstanceStatus'])
        while res['DBInstances'][0]['DBInstanceStatus'] == 'creating':
            sleep(15)
            res = rds.describe_db_instances(
        DBInstanceIdentifier='shreydbid'
            )
        return  res['DBInstances'][0]['Endpoint']

if __name__ == "__main__":
    
    Endpoint=create_rds_instance()
    startup_script1 = """#!/bin/bash
yum update -y
yum install docker -y
service docker start
systemctl enable docker.service

mkdir /cn_microservice
aws s3 sync s3://shreyas-bucket12/lab8/cn_microservice /cn_microservice
cd /cn_microservice/
echo 'const endpoint = "{}";module.exports=endpoint;' >> endpoint.js
docker build -t cn_microservice .
docker run -d -p 80:8081 -t cn_microservice
""".format(Endpoint['Address'])
    
    startup_script2="""#!/bin/bash
yum update -y
yum install docker -y
service docker start
systemctl enable docker.service

mkdir /fb_microservice
aws s3 sync s3://shreyas-bucket12/lab8/fb_microservice /fb_microservice
cd /fb_microservice/
echo 'const endpoint = "{}";module.exports=endpoint;' >> endpoint.js
docker build -t fb_microservice .

docker run -d -p 80:8082 -t fb_microservice
""".format(Endpoint['Address'])
    

    startup_script3="""#!/bin/bash
yum update -y
yum install docker -y
service docker start
systemctl enable docker.service

mkdir /like_microservice
aws s3 sync s3://shreyas-bucket12/lab8/like_microservice /like_microservice
cd /like_microservice/
echo 'const endpoint = "{}";module.exports=endpoint;' >> endpoint.js
docker build -t like_microservice .

docker run -d -p 80:8083 -t like_microservice
""".format(Endpoint['Address'])
    


    instance_response = create_instance(startup_script1)
    instance_response = create_instance(startup_script2)
    instance_response = create_instance(startup_script3)

    
