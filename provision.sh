#!/bin/bash
set -e

install_base_tools() {
  sudo apt-get update
  sudo apt-get install -y ca-certificates curl gnupg lsb-release
}

install_docker() {
  sudo apt-get install -y docker.io docker-compose
  sudo systemctl enable docker
  sudo systemctl start docker
  sudo usermod -aG docker vagrant
}

install_dev_tools() {
  sudo apt-get install -y make python3-pip
}

verify_installation() {
  docker --version
  docker-compose --version
  make --version
  pip3 --version
}

main() {
  install_base_tools
  install_docker
  install_dev_tools
  verify_installation
}

main
