import cv2
from flask import Flask, Response

app = Flask(__name__)

def generate_frames():
    camera = cv2.VideoCapture(0)

    camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))  # MJPG peut parfois forcer la couleur
    camera.set(cv2.CAP_PROP_CONVERT_RGB, 1)  # Assure la conversion en RGB si supporté

    while True:
        ret, frame = camera.read()
        if not ret:
            break

        frame = cv2.rotate(frame, cv2.ROTATE_180)  # Rotation 180°

        success, buffer = cv2.imencode('.jpg', frame)
        if not success:
            print("Erreur d'encodage !")
            continue  # Ignore l'image si l'encodage échoue

        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    camera.release()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
