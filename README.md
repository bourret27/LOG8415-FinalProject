# LOG8415E - Final Project
Final project for LOG8415

## Prerequisites
In order to run this solution you must do the following:  
1. Install [Docker Engine](https://docs.docker.com/get-docker/) 
2. Fill in the `.env` file with your AWS CLI credentials 
3. In the `infrastructure_builder.py` file, replace the `SUBNET_ID` with your subnet id. This can be found in the AWS console on the "VPC" page, under the "Subnets" option.
4. Copy your `.pem` access key in the repository. 

## Benchmarking 

In order to generate the instances needed for this solution, simply run `./run.sh`. This will generate the Docker container that will be used setup the instances.

### Benchmarking the MySQL Standalone server

To benchamrk the MySQL Standalone server, connect to the server named "Standalone" vis SSH, and copy the commands from the `setup_scripts/standalone.sh` or simply copy the file on the instance using `scp` and your access key and run the script.

Make sure to run the commands as the `root` user. In order to do so, run `sudo -s`  

The results will be under `/ubuntu/home/results.txt`.

### Benchmarking the MySQL Cluster

First off, as root user on the master instance (named "master"), you must copy and run the commands on from the `setup_scripts/master.sh` file in order too set up the master node.

Next, on each of the slaves (named "slave_1", "slave_2" and "slave_3"), as root user, you must copy and run the commands found in `setup_scripts/slave.sh`. This will setup the slave nodes.

Finally, back on the master node, you must copy and run the commands found `setup_scripts/benchmark_cluster.sh`, that will run the benchmarking. The results will be under `/ubuntu/home/results.txt` on the master node.

## Proxy

Once the benchmarking is done, as root user once again on the Proxy server (named "proxy"): 

1. Copy the commands from the `setup_scripts/proxy.sh`.
2. `cd LOG8415-FinalProject`
3. Run `python3 proxy_app.py -p <implementation>` where `<implementation>` is either `direct`, `random` or `custom`.  

 

