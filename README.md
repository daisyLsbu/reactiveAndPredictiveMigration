# TelemetryApplication
Application to get the telemetry information, developed in python.
psutil library for system resource information for foot-printing application.
dockerstat api for the resources related to all the containers.
RTT data between the application host and the list of other hosts in the network.

# Setup:
1. Run the setup.sh (after uncommenting the text - for the first time)
2. run build.sh 
3. execute run.sh
OR
1. Install psutil and dockerpy libraries using pip install command.
2. Run the application with python app.py <port>.
Example : python app.py 5000
3. Open a web browser and go to http://localhost:<port>/ to see the UI

### Description
This is an example project that showcases how you can use the `psutil`
library to send metrics from your applications to a monitoring server written
in any language.

The included `app.py` file shows all the available apis 

### Running the Example
Use the setup and build script before starting the application or launch script can be used to run all 3 script at once.

use the following endpoints depending on the need:
/devicedetails : for the server metric
/containers : for docker metrics
/combined : for combined metrics
/rtt with host list in request body: to get rtt data in network 


if you need to run docker containers:
# dockerAPIs
Docker API usage: installation of docker and getting container metrics

Docker installation 
-------------------
1. Install Docker on your machine by following the instructions provided in the docker setup
2. To create your own cutom image folllow these steps:
### create custom image: install stress, python and add randomloop.py in container then build
sudo docker run -it ubuntu
sudo apt-get update -y
apt-get install -y stress-ng
apt-get install -y python3
chmod 777 looprandomstress.py 
docker cp looprandomstress.py 4d25f2399daa:/
docker images
docker image tag linuxubuntu-stress daisylsbu/linuxubuntu-stress:latest
docker image push daisylsbu/linuxubuntu-stress:latest


Notes:
Backup migrate and restore script for containers
Getting Container metrics using docker stats
