import cv2

camera = cv2.VideoCapture(0)

# Forcer la capture en couleur (si possible)
camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))  # MJPG peut parfois forcer la couleur
camera.set(cv2.CAP_PROP_CONVERT_RGB, 1)  # Assure la conversion en RGB si supporté
ret, frame = camera.read()

frame = cv2.rotate(frame, cv2.ROTATE_180)  # Rotation de 180°
if ret:
    print(f"Image capturée avec dimensions: {frame.shape}")  # Vérification des dimensions
    cv2.imwrite("test_image_color.jpg", frame)  # Enregistrer l'image
    print("Image enregistrée sous 'test_image_color.jpg'.")
else:
    print("Erreur: Impossible de capturer l'image.")

camera.release()
