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
sudo docker run -it <image-id>
sudo docker cp file <container-id>:<path>/<file-name>
chmod +x file
install stress ng: apt update; apt-get install stress
test stress script: stress -c 2 -i 1 -m 1 --vm-bytes 128M -t 10s

commit: sudo docker commit <id> name:version
save: sudo docker save -o /home/user/test_ubuntu.img name:version

sudo docker load -i img-name
sudo docker run -d name:version
sudo docker exec <container-id> cmd
docker build -t my_image .  # this will create an image with name "my_image" and it's tag is latest, if you want to give a different
#Uploading to GitHub cloud
docker commit <container id> username/repository:tag
docker push username/repository:tag

Notes:
Backup migrate and restore script for containers
Getting Container metrics using docker stats
