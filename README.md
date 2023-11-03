# MigrationOrchesTelemtry
The Application can monitor and collects data from the hosts in a network, monitor and stores the data and then orchestrate the migration of containers in the network.
It has three parts: telemetry data, monitoring/storing data, migration orchestration

# TelemetryApplication
Application to get the telemetry information, developed in python.
psutil library for system resource information for foot-printing application.
dockerstat api for the resources related to all the containers.
RTT data between the application host and the list of other hosts in the network.

# MonitoringApplication
The application runs continuously monitoring and storing data related to the hosts in the network.

Collects telemetry data from all the hosts in the network and stores in influx db.
Developed in python, list of host is provided in csv file.
AIOhttp for Asynchronous HTTP Client/Server communication with the hosts.
Timeseries Influx DB is used to store the data for all hosts. which can be used to plot and analyse using Grafana.

# MigrationOrchestrator
Orchestrates the migration of containers from the over-utilised host to a resource available host in the network.
The data stored in time-series influx DB is read continuously in a moving average for each of the host in the network.
The resource utilisation is converted to scalar and compared to the preset threshold.
For the over utilised hosts, its docker data is checked to identify the container/s to be migrated.
The available resources in the network is checked to identify the destination host/s.
The transmission time from the source host to destination hosts are checked to select the destination host.
The docker is used to host the containers, docker apis are used to aid migration from source to destination host. 
