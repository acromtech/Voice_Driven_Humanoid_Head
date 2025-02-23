import queue
import sounddevice as sd
import json
from vosk import Model, KaldiRecognizer, SetLogLevel
import os

# Réduire les détails de chargement
SetLogLevel(-1)


class AudioTranscription:
    def __init__(self, recording_device_name, target_sample_rate=16000):
        self.RECORDING_DEVICE_NAME = recording_device_name
        self.TARGET_SAMPLE_RATE = target_sample_rate

        # Charger le modèle Vosk
        MODEL_PATH = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "vosk_model"
        )
        print("Chargement du modèle Vosk...")
        self.model = Model(MODEL_PATH)
        self.recognizer = KaldiRecognizer(self.model, self.TARGET_SAMPLE_RATE)
        self.audio_queue = queue.Queue()

    def audio_callback(self, indata, frames, time, status):
        """Callback pour traiter l'entrée audio en temps réel."""
        if status:
            print(f"Statut : {status}")
        self.audio_queue.put(bytes(indata))

    def capture_and_transcribe(self):
        """Capture et transcrit l'audio en texte."""
        print("Démarrage de l'écoute... Parlez dans le microphone.")

        with sd.RawInputStream(
            samplerate=self.TARGET_SAMPLE_RATE,
            blocksize=8000,
            dtype="int16",
            channels=1,
            callback=self.audio_callback,
        ):
            while True:
                data = self.audio_queue.get()
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    texte = result.get("text", "")
                    if texte:
                        print(f"Texte transcrit : {texte}")
                        return texte


# Exécution principale (test)
if __name__ == "__main__":
    try:
        audio_transcription = AudioTranscription(
            recording_device_name="USB PnP Sound Device"
        )
        print(audio_transcription.capture_and_transcribe())
    except KeyboardInterrupt:
        print("\nProgramme arrêté.")
