#!/usr/bin/env python3
import time
from ingescape import *

# Configuration de l'agent
agent_name = "RaspberryAgent"
port = 5670

# Initialisation de l'agent
igs.agent_set_name(agent_name)
igs.definition_set_version("1.0")

# Création d'une sortie pour envoyer des données
igs.output_create("message", igs.STRING_T, None)

# Démarrer l'agent
igs.start_with_device(None, port)

try:
    while True:
        # Envoie un message toutes les 2 secondes
        igs.output_set_string("message", "Hello from Raspberry Pi!")
        print("Message envoyé : Hello from Raspberry Pi!")
        time.sleep(2)
except KeyboardInterrupt:
    print("\nArrêt de l'agent")
    igs.stop()
