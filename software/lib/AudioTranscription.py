import sounddevice as sd
import numpy as np
from scipy.signal import resample_poly
from faster_whisper import WhisperModel
import time
import wave

class AudioTranscription:
    def __init__(self, recording_device_name, playback_device_name, target_sample_rate=16000, mic_sample_rate=44100, silence_threshold=0.08, silence_duration=2, audio_file="test_audio.wav"):
        self.RECORDING_DEVICE_NAME = recording_device_name
        self.PLAYBACK_DEVICE_NAME = playback_device_name
        self.TARGET_SAMPLE_RATE = target_sample_rate
        self.MIC_SAMPLE_RATE = mic_sample_rate
        self.SILENCE_THRESHOLD = silence_threshold
        self.SILENCE_DURATION = silence_duration
        self.AUDIO_FILE = audio_file

        # Charger le modèle Faster-Whisper
        model_load_start = time.time()
        self.model = WhisperModel("tiny", device="cpu", compute_type="int8")  # Change to cuda for GPU acceleration
        model_load_end = time.time()
        print(f"Temps pour charger le modèle : {model_load_end - model_load_start:.2f} secondes")

        # Trouver les périphériques d'entrée
        try:
            self.recording_device = self.find_device_by_name(self.RECORDING_DEVICE_NAME, kind="input")
        except ValueError as e:
            print(f"Erreur lors de la configuration du périphérique : {e}")
            raise

    def find_device_by_name(self, name, kind="input"):
        devices = sd.query_devices()
        for idx, device in enumerate(devices):
            if name in device['name'] and device['max_input_channels' if kind == "input" else 'max_output_channels'] > 0:
                return idx
        raise ValueError(f"Device '{name}' not found for {kind}.")

    def is_voice_detected(self, audio_data):
        return np.max(np.abs(audio_data)) > self.SILENCE_THRESHOLD

    def capture_and_transcribe(self):
        print("Démarrage de l'écoute...")
        buffer = np.zeros(self.MIC_SAMPLE_RATE)  # Initialisation du buffer
        voice_detected = False
        last_voice_time = time.time()

        while True:
            try:
                # Capture d'un bloc audio
                audio_data = sd.rec(self.MIC_SAMPLE_RATE, samplerate=self.MIC_SAMPLE_RATE, channels=1, dtype='float32', device=self.recording_device)
                sd.wait()
            except Exception as e:
                print(f"Erreur lors de l'enregistrement audio : {e}")
                break

            if self.is_voice_detected(audio_data):
                if not voice_detected:
                    print("Voix détectée, début de l'enregistrement...")
                    voice_detected = True
                    buffer = audio_data
                else:
                    buffer = np.append(buffer, audio_data, axis=0)

                last_voice_time = time.time()
            else:
                # Si le silence dépasse la durée seuil, on arrête l'enregistrement
                if voice_detected and time.time() - last_voice_time > self.SILENCE_DURATION:
                    print("Silence détecté, démarrage de la transcription...")
                    transcribed_text = self.process_audio(buffer)
                    print("Texte transcrit :", transcribed_text)
                    voice_detected = False
                    buffer = np.zeros(self.MIC_SAMPLE_RATE)
                    break
        return transcribed_text

    def process_audio(self, recording):
        # Sauvegarde de l'enregistrement dans un fichier WAV
        with wave.open(self.AUDIO_FILE, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(self.MIC_SAMPLE_RATE)
            wav_file.writeframes((recording * 32767).astype(np.int16).tobytes())

        # Resampling avec scipy
        audio_data = recording.flatten()
        resampled_audio = resample_poly(audio_data, up=self.TARGET_SAMPLE_RATE, down=self.MIC_SAMPLE_RATE)

        # Transcription avec Faster-Whisper
        segments, _ = self.model.transcribe(resampled_audio, language="fr")
        return " ".join([segment.text for segment in segments])

# Exécution principale
if __name__ == "__main__":
    try:
        audio_transcription = AudioTranscription(recording_device_name="USB PnP Sound Device", playback_device_name="UACDemoV1.0")
        audio_transcription.capture_and_transcribe()
    except KeyboardInterrupt:
        print("\nProgramme arrêté.")

