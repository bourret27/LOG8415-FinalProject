from sshtunnel import SSHTunnelForwarder
import pymysql
import pandas as pd
import argparse

cluster_hosts = ['172.31.2.2', '172.31.2.3', '172.31.2.4', '172.31.2.5']
str_query = 'SELECT * FROM actor;'

def create_ssh_tunnel():
    print('Creating tunnel...')
    
    tunnel = SSHTunnelForwarder(
        (cluster_hosts[0], 22),
        ssh_username="ubuntu",
        ssh_pkey="labsuser.pem",
        local_bind_address=('127.0.0.1', 3306),
        remote_bind_address=('127.0.0.1', 3306)
    )
    tunnel.start()
    
    print('Tunnel creation successful!')

    return tunnel

def create_connection_to_db(hostname):
    connection = pymysql.connect(
        host=hostname,
        user='root',
        password='root',
        db="sakila",
        port=3306
    )

    return connection

def run_direct_hit():
    tunnel = create_ssh_tunnel()
    connection = create_connection_to_db(cluster_hosts[0])
    data = pd.read_sql_query(str_query, connection)
    print(data)

    return {}

def parse_arguments():
    parser = argparse.ArgumentParser(description='Proxy application')
    parser.add_argument('-p', required=True, choices=['direct', 'random', 'custom'])
    args = vars(parser.parse_args())
    return args

if __name__ == "__main__":
    args = parse_arguments()

    if args['p'] == 'direct':
        run_direct_hit()