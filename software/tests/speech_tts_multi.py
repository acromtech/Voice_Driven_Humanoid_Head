import os
import torch
from TTS.api import TTS

# Détecter si un GPU est disponible
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using device:", device)

# Initialiser TTS avec un modèle français
tts = TTS("tts_models/fr/mai/tacotron2-DDC")  # Ou un autre modèle français

# Texte à synthétiser
text = "Bonjour, comment ça va ?"

# Synthétiser le texte et sauvegarder dans un fichier
output_file = "output_fr.wav"
tts.tts_to_file(text=text, file_path=output_file)

# Optionnel : lire le fichier audio
os.system(f"xdg-open {output_file}")  # Pour Linux


