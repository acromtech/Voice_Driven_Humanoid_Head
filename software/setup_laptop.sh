#!/bin/bash

# Mettre à jour le système
echo "Mise à jour du système..."
sudo apt update && sudo apt upgrade -y

# Installer des utilitaires et bibliothèques nécessaires
echo "Installation des bibliothèques et outils nécessaires..."
sudo apt install -y libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev \
    ffmpeg \
    python3-dev \
    libsndfile1

cd ./software/lib
wget https://alphacephei.com/vosk/models/vosk-model-fr-0.22.zip
unzip vosk-model-fr-0.22.zip
rm -f vosk-model-fr-0.22.zip
mv vosk-model-fr-0.22 vosk_model

# Redémarrer pour appliquer les modifications
echo "Installation terminée. Un redémarrage est nécessaire pour appliquer les modifications."
echo "Voulez-vous redémarrer maintenant ? (y/n)"
read -r restart_choice
if [[ $restart_choice == "y" || $restart_choice == "Y" ]]; then
    sudo reboot
else
    echo "Redémarrez manuellement pour appliquer les modifications."
fi
