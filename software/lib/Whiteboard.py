import ingescape as igs

class Whiteboard:
    def __init__(self):
        pass

    def add_image(self, image_url, x, y):
        """Ajoute une image sur le tableau blanc."""
        igs.service_call("Whiteboard", "addImageFromUrl", (image_url, x, y), "")

    def add_shape(self, shape, x, y, width, height, color, rotation=0.0, transparency=0.0):
        """Ajoute une forme sur le tableau blanc."""
        igs.service_call("Whiteboard", "addShape", (shape, x, y, width, height, color, rotation, transparency), "")

    def chat(self, message_text):
        """Envoie un message sur le tableau blanc."""
        igs.service_call("Whiteboard", "chat", message_text, "")

    def clear(self):
        """Efface le contenu du tableau blanc."""
        igs.service_call("Whiteboard", "clear", None, "")

