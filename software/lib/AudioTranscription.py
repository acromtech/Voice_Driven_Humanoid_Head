import sounddevice as sd
import numpy as np
from scipy.signal import resample_poly
from faster_whisper import WhisperModel
import time
import wave
import queue

class AudioTranscription:
    def __init__(self, recording_device_name, playback_device_name, target_sample_rate=16000, mic_sample_rate=44100, speaker_sample_rate=48000, silence_threshold=0.08, silence_duration=2, audio_file="test_audio.wav"):
        self.RECORDING_DEVICE_NAME = recording_device_name
        self.PLAYBACK_DEVICE_NAME = playback_device_name
        self.TARGET_SAMPLE_RATE = target_sample_rate
        self.MIC_SAMPLE_RATE = mic_sample_rate
        self.SPEAKER_SAMPLE_RATE = speaker_sample_rate
        self.SILENCE_THRESHOLD = silence_threshold
        self.SILENCE_DURATION = silence_duration
        self.AUDIO_FILE = audio_file

        # Charger le modèle Faster-Whisper
        model_load_start = time.time()
        self.model = WhisperModel("base", device="cpu", compute_type="int8")
        model_load_end = time.time()
        print(f"Temps pour charger le modèle : {model_load_end - model_load_start:.2f} secondes")

        # Trouver les périphériques d'entrée et de sortie
        try:
            self.recording_device = self.find_device_by_name(self.RECORDING_DEVICE_NAME, kind="input")
            self.playback_device = self.find_device_by_name(self.PLAYBACK_DEVICE_NAME, kind="output")
        except ValueError as e:
            print(f"Erreur lors de la configuration des périphériques : {e}")
            raise

        # Initialisation de la queue pour stocker les messages transcrits
        self.transcription_queue = queue.Queue()

    def find_device_by_name(self, name, kind="input"):
        devices = sd.query_devices()
        for idx, device in enumerate(devices):
            if name in device['name'] and device['max_input_channels' if kind == "input" else 'max_output_channels'] > 0:
                return idx
        raise ValueError(f"Device '{name}' not found for {kind}.")

    def is_voice_detected(self, audio_data):
        return np.max(np.abs(audio_data)) > self.SILENCE_THRESHOLD

    def capture_and_transcribe(self, recording):
        # Sauvegarder l'enregistrement dans un fichier WAV
        file_save_start = time.time()
        print(f"Sauvegarde de l'enregistrement dans {self.AUDIO_FILE}...")
        with wave.open(self.AUDIO_FILE, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16 bits
            wav_file.setframerate(self.MIC_SAMPLE_RATE)
            wav_file.writeframes((recording * 32767).astype(np.int16).tobytes())
        file_save_end = time.time()
        print(f"Temps pour sauvegarder l'enregistrement : {file_save_end - file_save_start:.2f} secondes")

        # Resampling avec scipy
        resampling_start = time.time()
        print("Resampling avec scipy...")
        audio_data = recording.flatten()
        resampled_audio = resample_poly(audio_data, up=self.TARGET_SAMPLE_RATE, down=self.MIC_SAMPLE_RATE)
        resampling_end = time.time()
        print(f"Temps pour le resampling : {resampling_end - resampling_start:.2f} secondes")

        # Transcription
        transcription_start = time.time()
        print("Transcription :")
        segments, info = self.model.transcribe(resampled_audio, language="fr")
        transcription_end = time.time()
        print(f"Temps pour la transcription : {transcription_end - transcription_start:.2f} secondes")

        # Retourner la transcription complète sous forme de phrase
        transcribed_text = " ".join([segment.text for segment in segments])
        return transcribed_text

    def listen_continuously(self):
        print("\nDémarrage de l'écoute continue...")
        buffer = np.zeros(self.MIC_SAMPLE_RATE)  # Buffer pour stocker l'audio
        voice_detected = False
        last_voice_time = time.time()

        while True:
            # Enregistrement en continu
            try:
                audio_data = sd.rec(self.MIC_SAMPLE_RATE, samplerate=self.MIC_SAMPLE_RATE, channels=1, dtype='float32', device=self.recording_device)
                sd.wait()
            except Exception as e:
                print(f"Erreur lors de l'enregistrement audio : {e}")
                break

            # Détecter la voix
            if self.is_voice_detected(audio_data):
                if not voice_detected:
                    print("Voix détectée, début de l'enregistrement...")
                    voice_detected = True
                    buffer = audio_data
                else:
                    buffer = np.append(buffer, audio_data, axis=0)

                # Mettre à jour l'heure du dernier son
                last_voice_time = time.time()
            else:
                if voice_detected and time.time() - last_voice_time > self.SILENCE_DURATION:
                    print("Silence détecté après la parole, envoi pour transcription...")
                    transcribed_text = self.capture_and_transcribe(buffer)
                    self.transcription_queue.put(transcribed_text)
                    print("Texte transcrit : ", transcribed_text)
                    voice_detected = False  # Réinitialiser l'état de voix détectée
                    buffer = np.zeros(self.MIC_SAMPLE_RATE)  # Réinitialiser le buffer
                    time.sleep(1)  # Pause avant de recommencer
                    
    def get_transcribed_message(self):
        # Récupérer le message transcrit depuis la queue
        try:
            return self.transcription_queue.get_nowait()  # Non-bloquant
        except queue.Empty:
            return None
            
    def stop(self):
        # Arrêter la transcription (par exemple, nettoyer les ressources)
        print("Arrêt de la transcription.")

# Test unitaire ou exécution directe
if __name__ == "__main__":
    # Crée un objet pour tester la transcription
    try:
        audio_transcription = AudioTranscription("Microphone", "Speaker")
        
        # Démarrer l'écoute continue dans un thread séparé
        from threading import Thread
        transcription_thread = Thread(target=audio_transcription.listen_continuously, daemon=True)
        transcription_thread.start()

        # Tester la récupération du message transcrit
        for _ in range(5):
            message = audio_transcription.get_transcribed_message()
            if message:
                print(f"Message transcrit : {message}")
            time.sleep(1)

    except Exception as e:
        print(f"Erreur dans le test unitaire : {e}")

