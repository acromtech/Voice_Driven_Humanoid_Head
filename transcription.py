import whisper
import torch
import pyaudio
import numpy as np
import os
import sys

# Rediriger stderr vers os.devnull pour ne pas afficher les erreurs
sys.stderr = open(os.devnull, 'w')

class Transcription:
    def __init__(self):
        # Initialiser le modèle Whisper
        self.model = whisper.load_model("base")

        # Configuration audio
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK = 1024

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS,
                                   rate=self.RATE, input=True,
                                   frames_per_buffer=self.CHUNK)

    def detect_silence(self, audio_data, threshold=500):
        """Détecte si le niveau sonore est en dessous d'un certain seuil."""
        audio_array = np.frombuffer(audio_data, np.int16)
        return np.abs(audio_array).mean() < threshold

    def transcribe_audio(self):
        """Transcrit l'audio en continu et renvoie le texte transcrit."""
        print("Début de l'écoute...")
        audio_buffer = b""
        silence_duration = 0
        silence_threshold = 2  # secondes

        while True:
            # Lire le flux audio
            audio_data = self.stream.read(self.CHUNK)
            audio_buffer += audio_data

            if self.detect_silence(audio_data):
                silence_duration += self.CHUNK / self.RATE  # Calcule la durée de silence en secondes
            else:
                silence_duration = 0  # Réinitialiser si du son est détecté

            # Si le silence dure plus de 2 secondes, transcrire
            if silence_duration > silence_threshold:
                # Convertir le buffer en un format que Whisper peut utiliser
                audio_array = np.frombuffer(audio_buffer, np.int16).astype(np.float32) / 32768.0
                audio_buffer = b""  # Réinitialiser le buffer audio

                # Transcrire l'audio
                print("Transcription en cours...")
                result = self.model.transcribe(audio_array, language='fr')
                transcription_text = result['text']
                print("Transcription :", transcription_text)

                silence_duration = 0  # Réinitialiser le compteur de silence

                # Retourner le texte transcrit
                return transcription_text

    def stop(self):
        """Arrête le flux audio."""
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

if __name__ == "__main__":
    transcription = Transcription()
    try:
        text = transcription.transcribe_audio()
        print("Texte transcrit :", text)
    except KeyboardInterrupt:
        print("Arrêt de l'écoute.")
    finally:
        transcription.stop()

