from sshtunnel import SSHTunnelForwarder
import pymysql
import pandas as pd

if __name__ == "__main__":
    tunnel = SSHTunnelForwarder(
        ('172.31.2.2', 22),
        ssh_username="ubuntu",
        ssh_pkey="labsuser.pem",
        local_bind_address=('127.0.0.1', 3306),
        remote_bind_address=('127.0.0.1', 3306)
    )
    tunnel.start()

    str_query = 'SELECT * FROM actor;'
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        db="sakila",
        port=3306
    )

    data = pd.read_sql_query(str_query, conn)
    print("Hello World!")