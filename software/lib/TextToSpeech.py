import time
from gtts import gTTS
import sounddevice as sd
import tempfile
import os
import sys
import numpy as np
from pydub import AudioSegment


class TextToSpeech:
    def __init__(
        self, playback_device_name="UACDemoV1.0", sample_rate=48000, speed_factor=1.15
    ):
        """Initialise la classe avec des paramètres configurables"""
        self.playback_device_name = playback_device_name
        self.sample_rate = sample_rate
        self.speed_factor = speed_factor
        self.texts = {
            "fr": "Bonjour, ceci est un test en français.",
            "en": "Hello, this is a test in English.",
            "de": "Hallo, dies ist ein Test auf Deutsch.",
            "fi": "Hei, tämä on testi suomeksi.",
        }

    def generate_audio(self, lang, text=None):
        """Génère l'audio à partir du texte pour la langue spécifiée."""
        # Si aucun texte n'est fourni, utiliser le texte par défaut
        if text is None and lang in self.texts:
            text = self.texts[lang]
        elif lang not in self.texts:
            print(f"Language '{lang}' not supported.")
            return

        # Créer l'objet gTTS
        tts = gTTS(text=text, lang=lang, slow=False)

        # Sauvegarder dans un fichier temporaire
        with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as temp_file:
            tts.save(temp_file.name)

            # Charger l'audio avec pydub
            audio = AudioSegment.from_mp3(temp_file.name)

            # Ajuster la vitesse de l'audio en appliquant un étirement
            audio = audio.speedup(playback_speed=self.speed_factor)

            # Convertir l'audio pour qu'il corresponde à la fréquence d'échantillonnage du périphérique (48000 Hz)
            audio = audio.set_frame_rate(self.sample_rate)

            samples = np.array(audio.get_array_of_samples())

            # Obtenir l'index du périphérique par nom
            playback_device = self.get_device_by_name(self.playback_device_name)
            if playback_device is None:
                print(f"Device '{self.playback_device_name}' not found.")
                return

            # Lire l'audio avec sounddevice
            playback_start = time.time()
            print(f"Lecture avec le périphérique : {self.playback_device_name}")
            sd.play(samples, samplerate=self.sample_rate, device=playback_device)
            sd.wait()  # Attendre la fin de la lecture
            playback_end = time.time()

            print(
                f"Temps pour la lecture audio : {playback_end - playback_start:.2f} secondes"
            )

        print(f"Played audio for language: {lang}")

    def get_device_by_name(self, device_name):
        """Retourne l'index du périphérique correspondant au nom."""
        devices = sd.query_devices()
        for i, device in enumerate(devices):
            if device_name in device["name"]:
                return i
        return None

    def play_music(self, file_path):
        """Joue un fichier audio .mp3 spécifié."""
        if os.path.exists(file_path):
            audio = AudioSegment.from_mp3(file_path)

            # Ajuster la vitesse de l'audio en appliquant un étirement
            audio = audio.speedup(playback_speed=self.speed_factor)

            # Convertir l'audio pour qu'il corresponde à la fréquence d'échantillonnage du périphérique (48000 Hz)
            audio = audio.set_frame_rate(self.sample_rate)

            samples = np.array(audio.get_array_of_samples())

            # Obtenir l'index du périphérique par nom
            playback_device = self.get_device_by_name(self.playback_device_name)
            if playback_device is None:
                print(f"Device '{self.playback_device_name}' not found.")
                return

            # Lire l'audio avec sounddevice
            playback_start = time.time()
            print(
                f"Lecture de la musique avec le périphérique : {self.playback_device_name}"
            )
            sd.play(samples, samplerate=self.sample_rate, device=playback_device)
            sd.wait()
            playback_end = time.time()

            print(
                f"Temps pour la lecture audio : {playback_end - playback_start:.2f} secondes"
            )
            print(f"Played music from: {file_path}")
        else:
            print(f"The file '{file_path}' does not exist.")


if __name__ == "__main__":
    # Rediriger stderr vers /dev/null pour supprimer les messages d'erreur
    sys.stderr = open(os.devnull, "w")

    # Paramètres configurables par l'utilisateur
    playback_device_name = "UACDemoV1.0"  # Nom du périphérique audio
    sample_rate = 48000  # Fréquence d'échantillonnage
    speed_factor = 1.15  # Facteur de vitesse pour accélérer la voix

    # Initialiser la classe avec les paramètres configurés
    tts = TextToSpeech(
        playback_device_name=playback_device_name,
        sample_rate=sample_rate,
        speed_factor=speed_factor,
    )

    # Générer et lire l'audio pour chaque langue avec le texte par défaut
    for lang in tts.texts.keys():
        tts.generate_audio(lang)

    # Exemple de génération d'audio avec un texte personnalisé
    custom_text_fr = "Ceci est un texte personnalisé en Français"
    tts.generate_audio("fr", custom_text_fr)

    # Lire un fichier musical spécifique
    tts.play_music(
        "./data/monkey.mp3"
    )  # Assurez-vous que le fichier existe dans le même répertoire

    print("Test de Text-to-speech terminé.")
