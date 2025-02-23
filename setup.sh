#!/bin/bash

echo "System updates..."
sudo apt update && sudo apt upgrade -y

echo "uv project installations..."
sudo snap install astral-uv --classic
uv sync 

echo "Dependencies installation..."
sudo apt install -y 
    python3-picamera2 \
    libasound-dev \
    libportaudio2 \
    libportaudiocpp0 \
    portaudio19-dev \
    ffmpeg \
    python3-dev \
    libsndfile1

echo "Download & Install Vosk (fr) models..."
cd ./software/lib
wget https://alphacephei.com/vosk/models/vosk-model-fr-0.22.zip
unzip vosk-model-fr-0.22.zip
rm -f vosk-model-fr-0.22.zip
mv vosk-model-fr-0.22 vosk_model

# Configurer le SPI
echo "Activate SPI modules..."
if ! grep -q "^dtparam=spi=on" /boot/config.txt; then
    echo "dtparam=spi=on" | sudo tee -a /boot/config.txt
fi

if ! grep -q "^dtoverlay=spi0-2cs" /boot/config.txt; then
    echo "dtoverlay=spi0-2cs" | sudo tee -a /boot/config.txt
fi

if ! grep -q "^dtoverlay=spi1-2cs" /boot/config.txt; then
    echo "dtoverlay=spi1-2cs" | sudo tee -a /boot/config.txt
fi

echo "SSH activation..."
sudo systemctl enable ssh
sudo systemctl start ssh

echo "All packages installed. Reboot now (y/n)?"
read -r restart_choice
if [[ $restart_choice == "y" || $restart_choice == "Y" ]]; then
    sudo reboot
else
    echo "Reboot needed to apply modifications"
fi
