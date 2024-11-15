#!/bin/sh

# Mise à jour des paquets
sudo apt update

# Installation de ffmpeg pour le traitement audio
sudo apt install -y ffmpeg

# Installation de pip si ce n'est pas déjà fait
if ! command -v pip &> /dev/null
then
    sudo apt install -y python3-pip
fi

# Installation des bibliothèques Python nécessaires
sudo pip install gTTS pydub playsound
sudo pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116
sudo pip install git+https://github.com/openai/whisper.git
sudo apt install portaudio19-dev python3-pyaudio
sudo pip install pyaudio

echo "Installation des dépendances terminée. Veuillez vérifier que tout s'est bien installé."

