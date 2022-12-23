from sshtunnel import SSHTunnelForwarder
import pymysql

if __name__ == "__main__":
    tunnel = SSHTunnelForwarder(
        ('172.31.2.2', 22),
        ssh_username="ubuntu",
        ssh_pkey="labsuser.pem",
        local_bind_address=('127.0.0.1', 3306),
        remote_bind_address=('127.0.0.1', 3306)
    )
    tunnel.start()
    print("Hello World!")