import boto3
import infrastructure_builder



if __name__ == '__main__':
    ec2_client = boto3.client('ec2')
    ec2_resource = boto3.resource('ec2')
    security_group = infrastructure_builder.create_security_group(ec2_client, ec2_resource, 'custom_group')