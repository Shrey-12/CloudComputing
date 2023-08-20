import boto3
from time import sleep

def create_instance(startup_script):
    try:
        ec2=boto3.client('ec2',region_name='ap-south-1')
        # print(dir(ec2))
        reservation = ec2.run_instances(
            ImageId='ami-0da59f1af71ea4ad2',
            MaxCount=1,
            MinCount=1,
            InstanceType='t2.micro',
            KeyName='shreya-windows-12',
            SecurityGroups=['launch-wizard-1'],
            UserData=startup_script,
            IamInstanceProfile={
                'Arn': 'arn:aws:iam::677027043458:instance-profile/ec2_s3'
            }
        )
        instance=reservation['instances'][0]
        state = instance['State']['Name']
        while state == "pending":
            sleep(10)
            state = instance.update()
        if state=='running':
            print(f'Instance Public DNS: {}')

    except Exception as e:
        print(e)

    
if __name__=="__main__":
    startup_script="""#!/bin/bash
yum update -y
yum install httpd -y
systemctl start httpd.service
systemctl enable httpd
usermod -a -G apache ec2-user
chown -R ec2-user:apache /var/www
chmod 2775 /var/www
mkdir /var/www/html/
aws s3 sync s3://shreyas-bucket12/my-website /var/www/html/
systemctl restart httpd"""


 