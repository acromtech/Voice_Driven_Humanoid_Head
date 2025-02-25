#!/bin/bash

echo "System updates..."
sudo apt update && sudo apt upgrade -y

echo "uv project installations..."
sudo snap install astral-uv --classic
uv sync

echo "Dependencies installation..."
sudo apt install -y unzip
sudo apt install -y gcc
sudo apt install -y libcap-dev
sudo apt install -y libasound2-dev
sudo apt install -y libportaudio2
sudo apt install -y libportaudiocpp0
sudo apt install -y portaudio19-dev
sudo apt install -y ffmpeg
sudo apt install -y python3-dev
sudo apt install -y libsndfile1


echo "MediaPipe-rpi dependencies installation"
sudo apt install libxcb-shm0 libcdio-paranoia-dev libsdl2-2.0-0 libxv1  libtheora0 libva-drm2 libva-x11-2 libvdpau1 libharfbuzz0b libbluray2 libatlas-base-dev libhdf5-103 libgtk-3-0 libopenexr25
echo "Download & Install Vosk (fr) models..."
cd ./lib
wget https://alphacephei.com/vosk/models/vosk-model-fr-0.22.zip
unzip vosk-model-fr-0.22.zip
rm -f vosk-model-fr-0.22.zip
mv vosk-model-fr-0.22 vosk_model

# Configurer le SPI
echo "Activate SPI modules..."
if ! grep -q "^dtparam=spi=on" /boot/firmware/config.txt; then
    echo "dtparam=spi=on" | sudo tee -a /boot/firmware/config.txt
fi

if ! grep -q "^dtoverlay=spi0-2cs" /boot/firmware/config.txt; then
    echo "dtoverlay=spi0-2cs" | sudo tee -a /boot/firmware/config.txt
fi

if ! grep -q "^dtoverlay=spi1-2cs" /boot/firmware/config.txt; then
    echo "dtoverlay=spi1-2cs" | sudo tee -a /boot/firmware/config.txt
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
