import boto3

def create_security_group_standalone(client):
    security_group = client.create_security_group(
        GroupName='standalone_sg',
        Description='For standalone server.'
    )

    client.authorize_security_group_ingress(
        CidrIp='0.0.0.0/0',
        IpProtocol='tcp',
        FromPort=22,
        ToPort=22,
        GroupName='standalone_sg'
    )
        
    return security_group

def create_security_group(client, security_group_name, description):
    security_group = client.create_security_group(
        GroupName=security_group_name,
        Description=description
    )

    client.authorize_security_group_ingress(
        CidrIp='0.0.0.0/0',
        IpProtocol='-1',
        FromPort=0,
        ToPort=65535,
        GroupName=security_group_name
    )
        
    return security_group

def create_instances(client, instance_type, security_group_id, ip_address, instance_name):
        return client.run_instances(
            InstanceType=instance_type,
            MinCount=1,
            MaxCount=1,
            ImageId='ami-0574da719dca65348',
            KeyName='vockey',
            SecurityGroupIds=[security_group_id],
            SubnetId='subnet-01b5009d8894a05cc', # Subnet: 172.31.0.0/20 - diffrent ID depending on the user
            PrivateIpAddress=ip_address,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': instance_name
                        },
                    ]
                },
            ]
        )

