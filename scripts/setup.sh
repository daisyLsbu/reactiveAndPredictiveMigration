# This file is used in the new system to setup the git and download the telemetry project. uncomment the code below for first time installation.

#sudo apt update
#sudo apt install git
#git --version
#git clone -b monitor https://github.com/daisyLsbu/MigrationOrchesTelemtry.git
cd Monitor
git pull origin monitor
sudo apt install python3
sudo apt-get install python3-venv