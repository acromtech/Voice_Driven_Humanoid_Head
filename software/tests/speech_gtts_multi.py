from gtts import gTTS
import os
from playsound import playsound

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

    # Sauvegarde dans un fichier
    output_file = f"output_{lang}.mp3"
    tts.save(output_file)
    print(f"Saved: {output_file}")

    # Lecture du fichier audio (adapté selon le système)
    playsound(output_file)

print("Test multilingue terminé.")

