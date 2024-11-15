from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import tempfile
import os

# Dictionnaire avec le texte et les langues
texts = {
    'fr': "Bonjour, ceci est un test en français.",
    'en': "Hello, this is a test in English.",
    'de': "Hallo, dies ist ein Test auf Deutsch.",
    'fi': "Hei, tämä on testi suomeksi."
}

for lang, text in texts.items():
    # Création de l'objet gTTS
    tts = gTTS(text=text, lang=lang, slow=False)

    # Écrire dans un fichier temporaire
    with tempfile.NamedTemporaryFile(delete=True, suffix='.mp3') as temp_file:
        tts.save(temp_file.name)

        # Charger l'audio dans pydub
        audio = AudioSegment.from_mp3(temp_file.name)

        # Lecture de l'audio
        play(audio)

print("Test multilingue terminé.")

