#!/bin/bash

# Mettre à jour le système
echo "Mise à jour du système..."
sudo apt update && sudo apt upgrade -y

# Installer Python et pip (dernière version)
echo "Installation de Python et pip..."
sudo apt install -y python3 python3-pip

# Installer les dépendances Python
echo "Installation des dépendances Python..."
sudo pip3 install ingescape

# Redémarrer pour appliquer les modifications
echo "Installation terminée. Un redémarrage est nécessaire pour appliquer les modifications."
echo "Voulez-vous redémarrer maintenant ? (y/n)"
read -r restart_choice
if [[ $restart_choice == "y" || $restart_choice == "Y" ]]; then
    sudo reboot
else
    echo "Redémarrez manuellement pour appliquer les modifications."
fi

