# Python script used on the proxy to run SQL queries on the SQL cluster

# To run, clone the git repository on the proxy server and run python3 proxy_app.py -p <impl> 
# where impl is direct, random or custom

import pythonping
import pymysql
import pandas as pd
import argparse
import random

from sshtunnel import SSHTunnelForwarder

cluster_hosts = ['172.31.2.2', '172.31.2.3', '172.31.2.4', '172.31.2.5']
str_query = 'SELECT * FROM actor;'

def create_ssh_tunnel():
    print('Creating tunnel...')
    
    tunnel = SSHTunnelForwarder(
        (cluster_hosts[0], 22),
        ssh_username="ubuntu",
        ssh_pkey="labsuser.pem",
        local_bind_address=('127.0.0.1', 3306), #SQL port
        remote_bind_address=('127.0.0.1', 3306)
    )
    tunnel.start()
    
    print('Tunnel creation successful!')

    return tunnel

def create_connection_to_db(hostname):
    print('Querying at ' + hostname + '...')

    connection = pymysql.connect(
        host=hostname,
        user='root',
        password='root',
        db="sakila",
        port=3306
    )
    
    print('Query sucessful!')
    
    return connection

def run_direct_hit():
    tunnel = create_ssh_tunnel()
    connection = create_connection_to_db(cluster_hosts[0])
    data = pd.read_sql_query(str_query, connection)
    connection.close()
    tunnel.close()
    print(data)

def run_random_hit():
    print('Choosing random server...')
    host = cluster_hosts[random.randint(1, 3)]
    print(host + ' is chosen.')

    tunnel = create_ssh_tunnel()
    connection = create_connection_to_db(host)
    data = pd.read_sql_query(str_query, connection)
    connection.close()
    tunnel.close()
    print(data)

def get_best_server():
    best_server = cluster_hosts[0]
    best_time = 1000
    
    print('Pinging all servers...')
    for host in cluster_hosts:
        result = pythonping.ping(host, count=1, timeout=5)

        if not(result.packet_loss) and result.rtt_avg_ms < best_time:
            print(host + ' - time: ' + str(result.rtt_avg_ms) + ' ms')
            best_server = host
            best_time = result.rtt_avg_ms
    
    print(best_server + ' is the best server.')
    return best_server

def run_custom_hit():
    host = get_best_server()
    tunnel = create_ssh_tunnel()
    connection = create_connection_to_db(host)
    data = pd.read_sql_query(str_query, connection)
    connection.close()
    tunnel.close()
    print(data)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Proxy application')
    parser.add_argument('-p', required=True, choices=['direct', 'random', 'custom'])
    args = vars(parser.parse_args())
    return args

if __name__ == "__main__":
    args = parse_arguments()

    if args['p'] == 'direct':
        print('Direct hit chosen.')
        run_direct_hit()
    
    elif args['p'] == 'random':
        print('Random hit chosen.')
        run_random_hit()

    elif args['p'] == 'custom':
        print('Custom hit chosen.')
        run_custom_hit()