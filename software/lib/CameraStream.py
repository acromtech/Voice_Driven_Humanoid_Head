import cv2
from picamera2 import Picamera2


class CameraStream:
    """Module de capture et d'affichage du flux vidéo de la caméra Raspberry Pi."""

    def __init__(self, resolution=(640, 480), framerate=30):
        self.picam2 = Picamera2()
        self.picam2.preview_configuration.main.size = resolution
        self.picam2.preview_configuration.main.format = "RGB888"
        self.picam2.preview_configuration.controls.FrameRate = framerate
        self.picam2.configure("preview")
        self.running = False

    def start_stream(self):
        """Démarre l'affichage du flux vidéo en temps réel."""
        self.picam2.start()
        self.running = True
        print("Flux vidéo démarré. Appuyez sur 'q' pour quitter.")

        while self.running:
            frame = self.picam2.capture_array()
            cv2.imshow("Camera Aramis", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                self.stop_stream()

    def stop_stream(self):
        """Arrête le flux vidéo proprement."""
        self.running = False
        self.picam2.stop()
        cv2.destroyAllWindows()
        print("Flux vidéo arrêté.")


if __name__ == "__main__":
    try:
        camera = CameraStream()
        camera.start_stream()
    except KeyboardInterrupt:
        print("\nArrêt du test caméra.")
        camera.stop_stream()
