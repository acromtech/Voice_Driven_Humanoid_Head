#!/bin/bash

# Mettre à jour le système
echo "Mise à jour du système..."
sudo apt update && sudo apt upgrade -y

# Installer Python et pip (dernière version)
echo "Installation de Python et pip..."
sudo apt install -y python3 python3-pip

# Installer les dépendances Python
echo "Installation des dépendances Python..."
sudo pip3 install \
    gTTS \
    pydub \
    playsound \
    torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116 \
    numpy==1.24.0 \
    git+https://github.com/openai/whisper.git \
    faster-whisper \
    pillow \
    sounddevice \
    scipy \
    can \
    ingescape

# Installer des utilitaires et bibliothèques nécessaires
echo "Installation des bibliothèques et outils nécessaires..."
sudo apt install -y libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev \
    ffmpeg \
    python3-dev \
    libsndfile1

# Configurer le SPI
echo "Activation des modules SPI..."
if ! grep -q "^dtparam=spi=on" /boot/config.txt; then
    echo "dtparam=spi=on" | sudo tee -a /boot/config.txt
fi

if ! grep -q "^dtoverlay=spi0-2cs" /boot/config.txt; then
    echo "dtoverlay=spi0-2cs" | sudo tee -a /boot/config.txt
fi

if ! grep -q "^dtoverlay=spi1-2cs" /boot/config.txt; then
    echo "dtoverlay=spi1-2cs" | sudo tee -a /boot/config.txt
fi

# Activer l'accès SSH
echo "Activation de l'accès SSH..."
sudo systemctl enable ssh
sudo systemctl start ssh

# Redémarrer pour appliquer les modifications
echo "Installation terminée. Un redémarrage est nécessaire pour appliquer les modifications."
echo "Voulez-vous redémarrer maintenant ? (y/n)"
read -r restart_choice
if [[ $restart_choice == "y" || $restart_choice == "Y" ]]; then
    sudo reboot
else
    echo "Redémarrez manuellement pour appliquer les modifications."
fi

