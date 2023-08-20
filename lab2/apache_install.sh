#!/bin/bash

# Update the system
yum update

# Install Apache
yum install httpd

systemctl start httpd.service

# Enable Apache to start on boot
systemctl enable httpd
usermod -a -G apache ec2-user
chown -R ec2-user:apache /var/www
chmod 2775 /var/www

# Create a directory for the website files
mkdir /var/www/html/

# # Copy the website files from S3 to the instance
# aws s3 sync s3://shreyas-bucket12/my-website /var/www/html/
echo "2101036" > /var/www/html/index.html

# Restart Apache
systemctl restart httpd