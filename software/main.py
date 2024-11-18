from lib.TextToSpeech import TextToSpeech
from lib.Decision import Decision
from lib.AudioTranscription import AudioTranscription
from lib.AnimatedScreen import AnimatedScreen  # Assure-toi d'importer AnimatedScreen
import time
import threading

def main():
    # Initialize modules
    text_to_speech = TextToSpeech(playback_device_name="UACDemoV1.0", sample_rate=48000, speed_factor=1.15)
    decision = Decision()
    audio_transcription = AudioTranscription(recording_device_name = "USB PnP Sound Device", playback_device_name = "UACDemoV1.0", speaker_sample_rate=48000, silence_threshold=0.08, silence_duration=2)

    # Initialize the screens
    bus_eyes = 0
    rst_eye_left = 27
    dc_eye_left = 25
    bl_eye_left = 23
    device_eye_left = 0

    rst_eye_right = 22
    dc_eye_right = 24
    bl_eye_right = 26
    device_eye_right = 1

    bus_mouth = 1
    rst_mouth = 5
    dc_mouth = 19
    bl_mouth = 6
    device_mouth = 0

    # Initialize the animated screens for eyes and mouth
    eye_left = AnimatedScreen(bus_eyes, device_eye_left, rst_eye_left, dc_eye_left, bl_eye_left)
    eye_right = AnimatedScreen(bus_eyes, device_eye_right, rst_eye_right, dc_eye_right, bl_eye_right)
    mouth = AnimatedScreen(bus_mouth, device_mouth, rst_mouth, dc_mouth, bl_mouth)

    # Lancer le thread pour l'écoute continue
    transcription_thread = threading.Thread(target=audio_transcription.listen_continuously, daemon=True)
    transcription_thread.start()

    try:
        while True:
            print("Waiting for a voice command...")

            # Attendre qu'une transcription soit disponible
            message_text = audio_transcription.get_transcribed_message()
            if message_text:
                print(f"Received command: {message_text}")

                # Get the corresponding response
                answer_text, answer_move, answer_eyes, answer_mouth = decision.get_response(message_text)
                print(f"Response: {answer_text}")
                print(f"Planned movement: {answer_move}")
                print(f"Eye animation: {answer_eyes}")
                print(f"Mouth animation: {answer_mouth}")

                # Add the response to the whiteboard
                # whiteboard.chat(answer_text)
                
                # Play GIF animation eyes
                if answer_eyes == "blink_fast":
                    print("Opening eyes...")
                    eye_left.openEye()
                    eye_right.openEye()
                elif answer_eyes == "smile":
                    print("Closing eyes...")
                    eye_left.closeEye()
                    eye_right.closeEye()
                else:
                    print("No eye animation specified.")
                
                # Play GIF animation mouth
                if answer_mouth == "open":
                    print("Playing smile GIF for the mouth...")
                    mouth.display_gif('./pic/open.gif', delay=0.1)
                elif answer_mouth == "close":
                    print("Playing frown GIF for the mouth...")
                    mouth.display_gif('./pic/close.gif', delay=0.1)
                else:
                    print("No mouth animation specified.")
                
                # Play the vocal response
                text_to_speech.generate_audio('fr', answer_text)

            # Simuler une petite pause avant la prochaine itération
            time.sleep(1)

    except KeyboardInterrupt:
        print("Stopping the program.")
    finally:
        audio_transcription.stop()  # Appeler stop pour la classe AudioTranscription
        eye_left.clear()  # Clear the eye screens when stopping
        eye_right.clear()
        mouth.clear()  # Clear the mouth screen

if __name__ == "__main__":
    main()

