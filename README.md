# Orchestrator
The application will collect metrics from all the servers mentioned in the host.csv file, store it
in influx db and does orchestration for the migration

for setting up this telemetry application follow the steps:

# installation
Run the setup.sh (after uncommenting the text - for the first time)
run build.sh
update host.csv file with the hosts to be monitored in the network
To check if everything is working fine, you can use collectDisplayTable.py file and follow instrauction
update the influx DB credential in influcDBsuite.py
execute run.sh
Note :
1. The server should have python 3 installed on them.


