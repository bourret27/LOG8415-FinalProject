from sshtunnel import SSHTunnelForwarder
import pymysql
import pandas as pd

def create_ssh_tunnel():
    tunnel = SSHTunnelForwarder(
        ('172.31.2.2', 22),
        ssh_username="ubuntu",
        ssh_pkey="labsuser.pem",
        local_bind_address=('127.0.0.1', 3306),
        remote_bind_address=('127.0.0.1', 3306)
    )
    tunnel.start()

    return tunnel

if __name__ == "__main__":
    tunnel = create_ssh_tunnel()
    str_query = 'SELECT * FROM actor;'
    conn = pymysql.connect(
        host='172.31.2.3',
        user='root',
        password='root',
        db="sakila",
        port=3306
    )

    data = pd.read_sql_query(str_query, conn)

    print(data)