#!/bin/bash

# Set variables
USER_HOME="/home/ahmed_masry_gcpcredits"
MINICONDA_PATH="$USER_HOME/miniconda3"
ENV_NAME="osworld"

# Install Miniconda
cd "$USER_HOME"
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
bash miniconda.sh -b -p "$MINICONDA_PATH"

# Initialize conda manually for this script
export PATH="$MINICONDA_PATH/bin:$PATH"
source "$MINICONDA_PATH/etc/profile.d/conda.sh"

# Create and activate conda env
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
conda create -n "$ENV_NAME" python=3.9 -y
conda activate "$ENV_NAME"


# Install gcsfuse
# wget https://github.com/GoogleCloudPlatform/gcsfuse/releases/download/v3.0.1/gcsfuse_3.0.1_amd64.deb
# sudo dpkg -i gcsfuse_3.0.1_amd64.deb

# Install Docker
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
sudo docker run hello-world

cd OSWorld

sudo apt-get update
sudo apt-get install linux-headers-$(uname -r)
sudo apt-get install build-essential python3-dev -y
pip install -r requirements.txt
pip install borb==2.1.25
sudo apt-get install libgl1-mesa-glx libsm6 libxext6 libxrender1 libfontconfig1 libice6 -y
pip install google-cloud
pip install google-cloud-vision

# Add docker permissions
sudo usermod -aG docker ahmed_elmasry24653
