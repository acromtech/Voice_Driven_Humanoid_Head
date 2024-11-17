from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import tempfile
import os
import sys

class SyntheseVocale:
    def __init__(self):
        self.texts = {
            'fr': "Bonjour, ceci est un test en français.",
            'en': "Hello, this is a test in English.",
            'de': "Hallo, dies ist ein Test auf Deutsch.",
            'fi': "Hei, tämä on testi suomeksi."
        }

    def generate_audio(self, lang, text=None):
        """Génère un audio à partir du texte pour la langue spécifiée."""
        # Si aucun texte n'est fourni, utiliser le texte par défaut
        if text is None and lang in self.texts:
            text = self.texts[lang]
        elif lang not in self.texts:
            print(f"Langue '{lang}' non supportée.")
            return

        # Création de l'objet gTTS
        tts = gTTS(text=text, lang=lang, slow=False)

        # Écrire dans un fichier temporaire
        with tempfile.NamedTemporaryFile(delete=True, suffix='.mp3') as temp_file:
            tts.save(temp_file.name)

            # Charger l'audio dans pydub
            audio = AudioSegment.from_mp3(temp_file.name)

            # Lecture de l'audio
            play(audio)

        print(f"Played audio for language: {lang}")

    def play_music(self, file_path):
        """Joue un fichier audio .mp3 spécifié."""
        if os.path.exists(file_path):
            audio = AudioSegment.from_mp3(file_path)
            play(audio)
            print(f"Played music from: {file_path}")
        else:
            print(f"Le fichier '{file_path}' n'existe pas.")

if __name__ == "__main__":
    # Rediriger stderr vers /dev/null pour supprimer les messages d'erreur
    sys.stderr = open(os.devnull, 'w')

    synthese_vocale = SyntheseVocale()

    # Génération et lecture de l'audio pour chaque langue avec texte par défaut
    for lang in synthese_vocale.texts.keys():
        synthese_vocale.generate_audio(lang)

    # Exemples de génération audio avec texte personnalisé
    custom_text_fr = "Ceci est un texte personnalisé en français."
    synthese_vocale.generate_audio('fr', custom_text_fr)

    # Lecture d'une musique spécifique
    synthese_vocale.play_music("monkey.mp3")  # Assurez-vous que le fichier existe dans le même répertoire

    print("Test de synthèse vocale terminé.")

