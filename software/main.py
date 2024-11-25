import time
import threading
from lib.AudioTranscription import AudioTranscription
from lib.Decision import Decision
from lib.TextToSpeech import TextToSpeech

simulation_mode = False

def execute_eyes_animation(eyes, answer_eyes):
    eyes.gif_choice_eyes(answer_eyes, speed_multiplier=1.0)
    print("execute anim:", answer_eyes)

def execute_mouth_animation(mouth, answer_mouth):
    mouth.gif_choice_mouth(answer_mouth, speed_multiplier=1.0)
    print("execute anim:", answer_mouth)

def execute_movement(answer_move):
    if answer_move:
        print(f"Executing movement: {answer_move}")
        # Simule l'exécution du mouvement (remplace par ton code de contrôle moteur)
        time.sleep(1)
    else:
        print("No movement specified.")

def execute_tts(text_to_speech, answer_text):
    text_to_speech.generate_audio('fr', answer_text)

def main():
    # Initialize modules
    if simulation_mode == False:
        from lib.AnimatedScreen import AnimatedScreen
        eyes = AnimatedScreen(bus=0, device=0, rst=27, dc=25, bl=23)
        mouth = AnimatedScreen(bus=1, device=0, rst=5, dc=19, bl=6)
    text_to_speech = TextToSpeech(playback_device_name="UACDemoV1.0", sample_rate=48000, speed_factor=1.15)
    audio_transcription = AudioTranscription(recording_device_name="USB PnP Sound Device", playback_device_name="UACDemoV1.0", mic_sample_rate=44100, silence_threshold=0.02, silence_duration=0.5) 
    decision = Decision(device="wlan0", simulation_mode=simulation_mode)

    try:
        print("Waiting for a voice command...")
        while True:
            # Processus de décision
            message_text = audio_transcription.capture_and_transcribe()

            if message_text:
                print(f"Received command: {message_text}")
                answer_text, answer_move, answer_eyes, answer_mouth = decision.get_response(message_text)
                print(f"Response: {answer_text}")
                print(f"Planned movement: {answer_move}")
                print(f"Eye animation: {answer_eyes}")
                print(f"Mouth animation: {answer_mouth}")
                if simulation_mode == False:
                    # Threads pour les différentes actions
                    threads = [
                        threading.Thread(target=text_to_speech.generate_audio, args=('fr', answer_text)),
                        threading.Thread(target=execute_eyes_animation, args=(eyes, answer_eyes)),
                        threading.Thread(target=execute_mouth_animation, args=(mouth, answer_mouth)),
                        threading.Thread(target=execute_movement, args=(answer_move)),
                    ]

                    # Démarrer tous les threads
                    for thread in threads:
                        thread.start()

                    # Attendre la fin de tous les threads
                    for thread in threads:
                        thread.join()

    except KeyboardInterrupt:
        print("Stopping the program.")
    finally:
        if simulation_mode == False:
            eyes.clear()
            mouth.clear()

if __name__ == "__main__":
    main()
