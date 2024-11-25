#!/bin/bash

# Mettre à jour le système
echo "Mise à jour du système..."
sudo apt update && sudo apt upgrade -y

# Installer Python et pip (dernière version)
echo "Installation de Python et pip..."
sudo apt install -y python3 python3-pip

# Installer les dépendances Python
echo "Installation des dépendances Python..."
sudo pip3 install gTTS
sudo pip3 install pydub
sudo pip3 install playsound
sudo pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116
sudo pip3 install numpy==1.24.0 
sudo pip3 install git+https://github.com/openai/whisper.git
sudo pip3 install faster-whisper
sudo pip3 install pillow
sudo pip3 install sounddevice
sudo pip3 install scipy
sudo pip3 install can
sudo pip3 install ingescape
sudo pip3 install spidev

# Installer des utilitaires et bibliothèques nécessaires
echo "Installation des bibliothèques et outils nécessaires..."
sudo apt install -y libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev \
    ffmpeg \
    python3-dev \
    libsndfile1

# Redémarrer pour appliquer les modifications
echo "Installation terminée. Un redémarrage est nécessaire pour appliquer les modifications."
echo "Voulez-vous redémarrer maintenant ? (y/n)"
read -r restart_choice
if [[ $restart_choice == "y" || $restart_choice == "Y" ]]; then
    sudo reboot
else
    echo "Redémarrez manuellement pour appliquer les modifications."
fi

