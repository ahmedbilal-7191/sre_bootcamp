#!/bin/bash
set -e
sudo apt-get update
sudo apt-get install -y docker.io docker-compose make
sudo groupadd docker || true
sudo usermod -aG docker $USER
newgrp docker
sudo systemctl enable docker
sudo systemctl start docker
docker --version
docker-compose --version
make --version
sudo apt-get install -y python3-pip
pip3 --version