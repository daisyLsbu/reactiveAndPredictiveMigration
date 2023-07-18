from .client import APIClient


""""
sudo docker run -it ubuntu bash

sudo docker container ls -- to know ids

sudo docker start <container-id>

sudo docker commit -p 6cb599fe30ea my-backup -- to take snapshot

sudo docker save -o ~/my-backup.tar my-backup


registry:


delete:


add:

docker hub: 
sudo docker login
sudo docker push my-backup:latest


;;;;;
$ sudo apt-get remove docker docker-engine docker.io containerd runc
2. Installing Docker Engine
$ sudo apt-get update
 
$ sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

$ sudo mkdir -p /etc/apt/keyrings
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

$ echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  
$ sudo apt-get update
$ sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin

$ sudo groupadd docker
$ sudo usermod -aG docker $USER
Check if docker is successfully installed in your system

$ sudo docker run hello-world

""""""