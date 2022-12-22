#!/bin/bash

apt-get update
apt-get install mysql-server sysbench -y

wget https://downloads.mysql.com/docs/sakila-db.tar.gz -O /home/ubuntu/sakila-db.tar.gz
tar -xvf /home/ubuntu/sakila-db.tar.gz -C /home/ubuntu/

mysql -u root -e "SOURCE /home/ubuntu/sakila-db/sakila-schema.sql;"
mysql -u root -e "SOURCE /home/ubuntu/sakila-db/sakila-data.sql;"

sysbench oltp_read_write --table-size=100000 --mysql-db=sakila --mysql-user=root prepare
sysbench oltp_read_write --table-size=100000 --threads=6 --max-time=60 --max-requests=0 --mysql-db=sakila --mysql-user=root run > /home/ubuntu/results.txt
sysbench oltp_read_write --mysql-db=sakila --mysql-user=root cleanup

