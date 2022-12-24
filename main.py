# Python script used to generate the instances necessary for the setup

# To run this script, simply turn on the Docker engine and run ./run.sh

import boto3
import infrastructure_builder

def create_proxy(client):
    security_group = infrastructure_builder.create_security_group(client, 'proxy_sg', 'For proxy.')
    proxy = infrastructure_builder.create_instances(client,'t2.large', security_group['GroupId'], '172.31.2.6', 'proxy')

    return proxy

def create_cluster_infrastructure(client):
    print('Creating infrastructure...')
    
    security_group = infrastructure_builder.create_security_group(client, 'cluster_sg', 'For SQL cluster.')

    master = infrastructure_builder.create_instances(client,'t2.micro', security_group['GroupId'], '172.31.2.2', 'master')

    slaves = []
    machine_address = 3
    for i in range(3):
        ip_address = '172.31.2.' + str(machine_address)
        instance_name = 'slave_' + str(i + 1)
        slave = infrastructure_builder.create_instances(client,'t2.micro', security_group['GroupId'], ip_address, instance_name)
        slaves.append(slave)
        machine_address += 1

    return master, slaves

    
def create_standalone_infrastructure(client):
    print('Creating infrastructure...')
    
    security_group = infrastructure_builder.create_security_group_standalone(client)
    standalone_server = infrastructure_builder.create_instances(client,'t2.micro', security_group['GroupId'], '172.31.2.1', 'standalone')
    
    return standalone_server


if __name__ == '__main__':
    ec2_client = boto3.client('ec2')

    #create_standalone_infrastructure(ec2_client)
    create_cluster_infrastructure(ec2_client)
    #create_proxy(ec2_client)
    