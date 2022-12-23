#!/bin/bash

# Install Python, Pip and Git
apt-get update
apt-get install python3 python3-pip git -y

# Install Python libraries needed to run application
pip install sshtunnel pythonping pymysql pandas argparse

# Clone project where the proxy application is found
git clone https://github.com/bourret27/LOG8415-FinalProject.git
