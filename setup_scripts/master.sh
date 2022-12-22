#!/bin/bash

apt-get update
apt-get libncurses5 libaio1 libmecab2 sysbench -y

cd /home/ubuntu
wget https://dev.mysql.com/get/Downloads/MySQL-Cluster-7.6/mysql-cluster-community-management-server_7.6.6-1ubuntu18.04_amd64.deb
dpkg -i mysql-cluster-community-management-server_7.6.6-1ubuntu18.04_amd64.deb

mkdir /var/lib/mysql-cluster
echo "
[ndbd default]
NoOfReplicas=2	

[ndb_mgmd]
hostname=198.51.100.2 
datadir=/var/lib/mysql-cluster 	

[ndbd]
hostname=198.51.100.0 
NodeId=2			
datadir=/usr/local/mysql/data	

[ndbd]
hostname=198.51.100.1 # Hostname/IP of the second data node
NodeId=3			
datadir=/usr/local/mysql/data	

[mysqld]

hostname=198.51.100.2 
" > /var/lib/mysql-cluster/config.ini

echo "
[Unit]
Description=MySQL NDB Cluster Management Server
After=network.target auditd.service

[Service]
Type=forking
ExecStart=/usr/sbin/ndb_mgmd -f /var/lib/mysql-cluster/config.ini
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
Restart=on-failure

[Install]
WantedBy=multi-user.target
" > /etc/systemd/system/ndb_mgmd.service

systemctl daemon-reload
systemctl enable ndb_mgmd
systemctl start ndb_mgmd

wget https://dev.mysql.com/get/Downloads/MySQL-Cluster-7.6/mysql-cluster_7.6.6-1ubuntu18.04_amd64.deb-bundle.tar
mkdir install
tar -xvf mysql-cluster_7.6.6-1ubuntu18.04_amd64.deb-bundle.tar -C install/
cd install

dpkg -i mysql-common_7.6.6-1ubuntu18.04_amd64.deb
dpkg -i mysql-cluster-community-client_7.6.6-1ubuntu18.04_amd64.deb
dpkg -i mysql-client_7.6.6-1ubuntu18.04_amd64.deb
dpkg -i mysql-cluster-community-server_7.6.6-1ubuntu18.04_amd64.deb
dpkg -i mysql-server_7.6.6-1ubuntu18.04_amd64.deb

echo "
!includedir /etc/mysql/conf.d/
!includedir /etc/mysql/mysql.conf.d/

[mysqld]
ndbcluster                   

[mysql_cluster]
ndb-connectstring=198.51.100.2 
" > /etc/mysql/my.cnf

systemctl restart mysql
systemctl enable mysql

cd /home/ubuntu
wget https://downloads.mysql.com/docs/sakila-db.tar.gz -O /home/ubuntu/sakila-db.tar.gz
tar -xvf /home/ubuntu/sakila-db.tar.gz -C /home/ubuntu/

mysql -u root -e "SOURCE /home/ubuntu/sakila-db/sakila-schema.sql;"
mysql -u root -e "SOURCE /home/ubuntu/sakila-db/sakila-data.sql;"

sysbench oltp_read_write --table-size=100000 --mysql-db=sakila --mysql-user=root prepare
sysbench oltp_read_write --table-size=100000 --threads=6 --max-time=60 --max-requests=0 --mysql-db=sakila --mysql-user=root run > /home/ubuntu/results.txt
sysbench oltp_read_write --mysql-db=sakila --mysql-user=root cleanup