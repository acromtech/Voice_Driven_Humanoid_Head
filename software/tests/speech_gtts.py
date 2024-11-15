from gtts import gTTS
import os
from playsound import playsound

# Texte à synthétiser
text = "Bonjour c'est mois Bob ton robot de compagnie ! Comment vas tu aujourd'hui ?"

# Créer un objet gTTS
tts = gTTS(text=text, lang='fr')

# Sauvegarder le fichier audio
audio_file = "output.mp3"
tts.save(audio_file)

# Lire le fichier audio
playsound(audio_file)

