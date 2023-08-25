import boto3
from time import sleep


def create_instances(startup_script):
    try:
        ec2 = boto3.client("ec2", region_name="ap-south-1")
        # print(dir(ec2))
        reservation = ec2.run_instances(
            ImageId="ami-0da59f1af71ea4ad2",
            MaxCount=1,
            MinCount=1,
            InstanceType="t2.micro",
            KeyName="shreya-windows-12",
            SecurityGroups=["launch-wizard-1"],
            UserData=startup_script,
            IamInstanceProfile={
                "Arn": "arn:aws:iam::677027043458:instance-profile/ec2_s3"
            },
        )
        instance_id = reservation["Instances"][0]["InstanceId"]
        print(f"Instance ID: {instance_id}")
        while True:
            desc = ec2.describe_instances(InstanceIds=[instance_id])
            inst = desc["Reservations"][0]["Instances"]
            temp = inst[0]
            if len(inst) == 0:
                print("[-]Instance not found")
                sleep(10)
            else:
                state = temp["State"]["Name"]
                if state == "pending":
                    print(f"[-]{state}")
                    sleep(10)
                    continue
                if state == "running":
                    print(f"[+] Congrats you finally completed the program!!!")
                    print(f"Public DNS Name: {temp['PublicDnsName']}")
                    break

    except Exception as e:
        print(e)


def list_running_instances(Reservations):
    for reservation in Reservations:
        for instance in reservation["Instances"]:
            print(instance["InstanceId"])


def check_health_status(Reservations):
    for reservation in Reservations:
        for instance in reservation["Instances"]:
            res = ec2.describe_instance_status(
                InstanceIds=[
                    instance["InstanceId"],
                ]
            )['InstanceStatuses'][0]
            print(res['InstanceStatus'], res["SystemStatus"])


def stop_running_instances(Reservations):
    for reservation in Reservations:
        for instance in reservation["Instances"]:
            ec2.stop_instances(InstanceIds=[instance["InstanceId"]])
            x = instance["InstanceId"]
            print(f"[-] {x} : Stopped")


def terminate_running_instances(Reservations):
    for reservation in Reservations:
        for instance in reservation["Instances"]:
            ec2.terminate_instances(InstanceIds=[instance["InstanceId"]])
            x = instance["InstanceId"]
            print(f"[-] {x} : Terminated")


if __name__ == "__main__":
    startup_script = """#!/bin/bash
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
    ec2 = boto3.client("ec2", region_name="ap-south-1")
    create_instances(startup_script)
    create_instances(startup_script)
    create_instances(startup_script)
    # sleep(30)
    response = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    Reservations = response["Reservations"]
    list_running_instances(Reservations)
    check_health_status(Reservations)
    stop_running_instances(Reservations)
    terminate_running_instances(Reservations)
