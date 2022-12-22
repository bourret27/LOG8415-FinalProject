import boto3
import infrastructure_builder
import argparse

def benchmark_cluster(client):
    return {}

def create_standalone_infrastructure(client):
    print('Creating infrastructure...')
    
    security_group = infrastructure_builder.create_security_group_standalone(client)
    
    user_data = open('standalone.sh', 'r').read()
    standalone_server = infrastructure_builder.create_instances(client,'t2.micro', 1, user_data, security_group['GroupId'], '172.31.2.1')
    
    return standalone_server

def benchmark_standalone(client):
    standalone_server = create_standalone_infrastructure(client)

    print('Benchmarking standalone server...')

    waiter = client.get_waiter('instance_status_ok')
    waiter.wait(InstanceIds=[standalone_server["Instances"][0]["InstanceId"]])

    print('Benchmarking complete! Results are available on standalone server in /home/ubuntu/results.txt.')

    
def parse_arguments():
    parser = argparse.ArgumentParser(description='LOG8415E - Final Project')
    parser.add_argument('-b', action='store_true')
    parser.add_argument('-p', required=True, choices=['direct', 'random', 'custom'])
    args = vars(parser.parse_args())
    return args


if __name__ == '__main__':
    args = parse_arguments()
    
    if(args['b']):
        print("Benchmarking!")

    if(args['p'] == 'direct'):
        print('Direct!')
    elif (args['p'] == 'random'):
        print('Random!')
    else:
        print('Custom!')

    ec2_client = boto3.client('ec2')
    benchmark_standalone(ec2_client)

    