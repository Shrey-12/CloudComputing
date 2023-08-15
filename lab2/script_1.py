import boto3
from time import sleep

def create_instance(startup_script):
    try:
        ec2=boto3.client('ec2',region_name='ap-south-1')
        # print(dir(ec2))
        instance = ec2.run_instances(
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
        #wait until the instance is running
        # instance.wait_until_running()
        state = instance.update()
        while state == "pending":
            sleep(5)
            state = instance.update()
            print(state) 
            
        #get the public DNS address of the instance
        public_dns=instance.public_dns_name
        return public_dns
    except Exception as e:
        print(e)

    
if __name__=="__main__":
    startup_script="""
#!/bin/bash
echo "shreya anant"  
    """
    public_dns=create_instance(startup_script)
    print(f'Public DNS: {public_dns}')

# systemctl start httpd.service
# systemctl enable httpd
# usermod -a -G apache ec2-user
# chown -R ec2-user:apache /var/www
# chmod 2775 /var/www
# echo "2101036" > /var/www/html/index.html
# systemctl restart httpd 
