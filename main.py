import boto3
import infrastructure_builder
import argparse

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

    """ec2_client = boto3.client('ec2')
    ec2_resource = boto3.resource('ec2')
    security_group = infrastructure_builder.create_security_group(ec2_client, ec2_resource, 'custom_group')"""