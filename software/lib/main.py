import time
import threading
from lib.AudioTranscription import AudioTranscription
from lib.Decision import Decision
from lib.Whiteboard import Whiteboard
from lib.TextToSpeech import TextToSpeech

simulation_mode = True

def execute_eyes_animation(eye_left, eye_right, answer_eyes):
    if answer_eyes == "blink_fast":
        print("Blinking eyes...")
        eye_left.openEye()
        eye_right.openEye()
    elif answer_eyes == "smile":
        print("Closing eyes...")
        eye_left.closeEye()
        eye_right.closeEye()
    else:
        print("No eye animation specified.")

def execute_mouth_animation(mouth, answer_mouth):
    if answer_mouth == "open":
        print("Playing smile GIF for the mouth...")
        mouth.display_gif('./pic/open.gif', delay=0.1)
    elif answer_mouth == "close":
        print("Playing frown GIF for the mouth...")
        mouth.display_gif('./pic/close.gif', delay=0.1)
    else:
        print("No mouth animation specified.")

def execute_movement(answer_move):
    if answer_move:
        print(f"Executing movement: {answer_move}")
        # Simule l'exécution du mouvement (remplace par ton code de contrôle moteur)
        time.sleep(1)
    else:
        print("No movement specified.")

def execute_tts(text_to_speech, answer_text):
    if answer_text:
        print(f"Playing TTS response: {answer_text}")
        text_to_speech.generate_audio('fr', answer_text)
    else:
        print("No text-to-speech response specified.")


def main():
    # Initialize modules
    if simulation_mode == False
        from lib.AnimatedScreen import AnimatedScreen
        eye_left = AnimatedScreen(bus_eyes=0, device_eye_left=0, rst_eye_left=27, dc_eye_left=25, bl_eye_left=23)
        eye_right = AnimatedScreen(bus_eyes=0, device_eye_right=1, rst_eye_right=22, dc_eye_right=24, bl_eye_right=26)
        mouth = AnimatedScreen(bus_mouth=1, device_mouth=0, rst_mouth=5, dc_mouth=19, bl_mouth=6)
    text_to_speech = TextToSpeech(playback_device_name="UACDemoV1.0", sample_rate=48000, speed_factor=1.15)
    audio_transcription = AudioTranscription(recording_device_name="USB PnP Sound Device", playback_device_name="UACDemoV1.0", mic_sample_rate=44100, silence_threshold=0.02, silence_duration=0.5) 
    decision = Decision()
    # whiteboard = Whiteboard(agent_name="Whiteboard", device="wlo1", port=5670)
    
    try:
        print("Waiting for a voice command...")
        while True:
            # Processus de décision
            message_text = audio_transcription.capture_and_transcribe()

            if message_text:
                print(f"Received command: {message_text}")
                # METTRE ICI L'ENVOIS DU MESSAGE TRANSCRIT VERS LE WHITEBOARD
                answer_text, answer_move, answer_eyes, answer_mouth = decision.get_response(message_text)
                print(f"Response: {answer_text}")
                print(f"Planned movement: {answer_move}")
                print(f"Eye animation: {answer_eyes}")
                print(f"Mouth animation: {answer_mouth}")
		        # METTRE ICI L'ENVOIS DU MESSAGE DE REPONSE VERS LE WHITEBOARD
		        text_to_speech.generate_audio('fr', answer_text)
		        
                if simulation_mode == False
                    # Threads pour les différentes actions
                    threads = [
                        threading.Thread(target=text_to_speech.generate_audio, args=('fr', answer_text)),
                        threading.Thread(target=execute_eyes_animation, args=(eye_left, eye_right, answer_eyes)),
                        threading.Thread(target=execute_mouth_animation, args=(mouth, answer_mouth)),
                        threading.Thread(target=execute_movement, args=(answer_move,)),
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
            eye_left.clear()
            eye_right.clear()
            mouth.clear()

if __name__ == "__main__":
    main()
