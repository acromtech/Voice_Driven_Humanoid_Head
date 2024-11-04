import whisper
import sounddevice as sd
import numpy as np
import queue
import threading

# Charger le modèle Whisper (choisir la taille du modèle selon votre préférence)
model = whisper.load_model("small")

# Configuration pour capturer l'audio
samplerate = 16000  # fréquence d'échantillonnage (Whisper utilise généralement 16000 Hz)
blocksize = 4000    # taille de bloc en échantillons (ajustable)
q = queue.Queue()

# Fonction pour l'enregistrement audio
def audio_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())

# Thread pour la transcription et l'écriture
def transcribe_audio():
    with open("transcription.txt", "a") as f:  # ouvrir le fichier en mode ajout
        while True:
            audio_data = q.get()  # récupérer les données audio
            # Transcrire avec Whisper
            result = model.transcribe(np.squeeze(audio_data))
            transcription = result["text"]
            print("Transcription: ", transcription)
            f.write(transcription + "\n")  # ajouter la transcription au fichier

# Démarrage du thread de transcription
thread = threading.Thread(target=transcribe_audio)
thread.daemon = True
thread.start()

# Démarrage de l'enregistrement
with sd.InputStream(samplerate=samplerate, channels=1, callback=audio_callback, blocksize=blocksize):
    print("Appuyez sur Ctrl+C pour arrêter l'enregistrement")
    while True:
        pass  # le script continue jusqu'à interruption
