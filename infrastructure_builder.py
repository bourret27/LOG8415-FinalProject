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

def create_instances(client, instance_type, count, user_data, security_group_id):
        return client.run_instances(
            InstanceType=instance_type,
            MinCount=count,
            MaxCount=count,
            ImageId='ami-0574da719dca65348',
            KeyName='vockey',
            UserData=user_data,
            SecurityGroupIds=[security_group_id]
        )