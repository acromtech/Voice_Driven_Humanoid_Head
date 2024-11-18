import sounddevice as sd
import numpy as np

# Configuration
MICRO_DEVICE = "hw:1,0"  # Microphone USB
SPEAKER_DEVICE = "hw:2,0"  # Haut-parleur USB
SAMPLE_RATE = 44100  # Taux d'échantillonnage (Hz)
DURATION = 5  # Durée de l'enregistrement (secondes)

def list_devices():
    """Affiche la liste des périphériques ALSA disponibles."""
    print("\nListe des périphériques audio disponibles :")
    print(sd.query_devices())

def test_record_playback():
    """Enregistre un extrait audio depuis un périphérique spécifique et le rejoue sur un autre."""
    try:
        print(f"\nEnregistrement pour {DURATION} secondes avec le micro ({MICRO_DEVICE})...")
        recording = sd.rec(
            int(SAMPLE_RATE * DURATION),
            samplerate=44100,
            channels=1,
            dtype='float32',
            device=MICRO_DEVICE,  # Spécifie le périphérique micro
        )
        sd.wait()  # Attente de la fin de l'enregistrement
        print("Enregistrement terminé !")

        print(f"\nLecture de l'enregistrement sur le haut-parleur ({SPEAKER_DEVICE})...")
        sd.play(recording, samplerate=48000, device=SPEAKER_DEVICE)  # Spécifie le périphérique haut-parleur
        sd.wait()  # Attente de la fin de la lecture
        print("Lecture terminée !")

    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    print("=== Test de configuration ALSA personnalisé ===")
    list_devices()
    test_record_playback()

