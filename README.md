# LOG8415E - Final Project
Final project for LOG8415

## Prerequisites
In order to run this solution you must do the following:  
1. Install [Docker Engine](https://docs.docker.com/get-docker/) 
2. Fill in the `.env` file with your AWS CLI credentials 
3. In the `infrastructure_builder.py` file, replace the `SUBNET_ID` with your subnet id. This can be found in the AWS console on the "VPC" page, under the "Subnets" option.

## Benchmarking 

In order to generate the instances needed for this solution, simply run `./run.sh`. This will generate the Docker container that will be used setup the instances.

### Benchmarking the MySQL Standalone server

To benchamrk the MySQL Standalone server, connect to the server named "Standalone" vis SSH, and copy the commands from the `setup_scripts/standalone.sh` or simply copy the file on the instance using `scp` and your access key and run the script.

Make sure to run the commands as the `root` user. In order to do so, run `sudo -s`  

The results will be under `/ubuntu/home/results.txt`.

### Benchmarking the SQL Cluster

First off, as root user on the first slave (named "slave_1"), you must copy the copy the commands from the `setup_scripts/slave.sh` file. Repeat this step for the other slaves ("slave_2" and "slave_3").

On the master node (named "master"), as root user, copy the the commands from the `setup_scripts/master.sh` file. This will then run the benchmarking of the cluster node. The results will be under `/ubuntu/home/results.txt`.

## Proxy

Once the benchmarking is done, as root user once again on the proxy server (named "proxy"): 

1. Copy the commands from the `setup_scripts/proxy.sh`.
2. `cd LOG8415-FinalProject`
3. Run `python3 proxy_app.py -p <implementation>` where `<implementation>` is either `direct`, `random` or `custom`.  

 

