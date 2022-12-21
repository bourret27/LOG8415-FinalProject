import boto3

def create_security_group(client, resource, security_group_name):
    response_vpcs = client.describe_vpcs()
    vpc_id = response_vpcs.get('Vpcs', [{}])[0].get('VpcId', '')

    response_security_group = client.create_security_group(
        GroupName=security_group_name,
        Description='Security group for our instances',
        VpcId=vpc_id)

    security_group_id = response_security_group['GroupId']
        
    client.authorize_security_group_ingress(
    GroupId=security_group_id,
    IpPermissions=[
        {'IpProtocol': 'tcp',
            'FromPort': 80,
            'ToPort': 80,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
        {'IpProtocol': 'tcp',
            'FromPort': 22,
            'ToPort': 22,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ])
        
    return resource.SecurityGroup(response_security_group['GroupId'])