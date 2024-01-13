# MonitoringApplication
The application runs continuously monitoring and storing data related to the hosts in the network.
The application will collect metrics from all the servers mentioned in the host.csv file, store it
in influx db and does orchestration for the migration

Collects telemetry data from all the hosts in the network and stores in influx db.
Developed in python, list of host is provided in csv file.
AIOhttp for Asynchronous HTTP Client/Server communication with the hosts.
Time-series Influx DB is used to store the data for all hosts. which can be used to plot and analyse using Grafana.
# Requirement
InfluxDBClient for connecting to Influx DB server.
Grafana to manage and monitor processes.
## Installation
Run the setup.sh (after uncommenting the text - for the first time)
run build.sh
update host.csv file with the hosts to be monitored in the network
## Test
To check if everything is working fine, you can use collectDisplayTable.py file and follow instruction
update the influx DB credential in influcDBsuite.py
execute run.sh
This will display the collected data on your terminal. If Grafana is running then it should reflect there
as well.
Note: The code assumes that the user has access to a local instance of InfluxDB
and Grafana. Please make sure to install and configure them properly before using this software.</s>

use test_data.json file for sample data

# MigrationOrchestrator
Orchestrates the migration of containers from the over-utilised host to a resource available host in the network.
The data stored in time-series influx DB is read continuously in a moving average for each of the host in the network.
The resource utilisation is converted to scalar and compared to the preset threshold.
For the over utilised hosts, its docker data is checked to identify the container/s to be migrated.
The available resources in the network is checked to identify the destination host/s.
The transmission time from the source host to destination hosts are checked to select the destination host.
The docker is used to host the containers, docker apis are used to aid migration from source to destination host. 

Once a suitable destination host has been selected, it will start transferring the docker image of the identified containers after stopping the container.
ssh is used to transfer the image between hosts as implemented in connectRemote.py

### Prerequisites:
1. The orchestration framework should have access to all relevant information about the infrastructure (eg., IP addresses of machines, their capacity, current load).
2. Each machine must run a daemon that provides information about CPU usage, memory usage, etc
3. There should be an API for querying these metrics. This can be done using any language




