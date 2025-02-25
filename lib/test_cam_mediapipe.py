import cv2
import mediapipe as mp
from flask import Flask, Response

app = Flask(__name__)

# Initialisation de MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def generate_frames():
    camera = cv2.VideoCapture(0)

    while True:
        ret, frame = camera.read()
        if not ret:
            break

        # Rotation 180° pour aligner avec ton flux existant
        frame = cv2.rotate(frame, cv2.ROTATE_180)
        frame = cv2.resize(frame, (1280, 720))  

        # Conversion en RGB (MediaPipe attend une image en RGB, OpenCV est en BGR)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Détection des mains
        results = hands.process(rgb_frame)

        # Dessin des landmarks si une main est détectée
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Encodage en JPEG pour le flux
        success, buffer = cv2.imencode('.jpg', frame)
        if not success:
            continue  # Ignore l’image si l’encodage échoue

        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    camera.release()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
