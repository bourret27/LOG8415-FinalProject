import boto3

def create_security_group(client, security_group_name, description):
    
    security_group = client.create_security_group(
        GroupName=security_group_name,
        Description=description
    )

        
    client.authorize_security_group_ingress(
        CidrIp='0.0.0.0/0',
        IpProtocol='tcp',
        FromPort=22,
        ToPort=22,
        GroupName=security_group_name
   
    )
        
    return security_group

def create_instances(client, instance_type, count, image_id, key, user_data, security_group_id):
        return client.run_instances(
            InstanceType=instance_type,
            MinCount=count,
            MaxCount=count,
            ImageId=image_id,
            KeyName=key,
            UserData=user_data,
            SecurityGroupIds=[security_group_id]
        )