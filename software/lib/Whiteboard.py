import ingescape as igs
import time


class Whiteboard:
    def __init__(self, agent_name="Whiteboard", device="Wi-Fi", port=5670):
        """Initialisation de l'agent et des configurations de base."""
        self.agent_name = agent_name
        self.device = device
        self.port = port

        # Configuration de l'agent
        igs.agent_set_name(self.agent_name)

        # Observation des inputs
        igs.observe_input("message_text", Message_Text_input_callback, self)

        # Démarrage de l'agent
        igs.start_with_device(self.device, self.port)
        time.sleep(2)  # Pause pour s'assurer que le service démarre correctement

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


def Message_Text_input_callback(io_type, name, value_type, value, my_data):
    """Callback pour la réception de messages."""
    try:
        agent_object = my_data
        assert isinstance(agent_object, Whiteboard)
        agent_object.chat("hello")
    except Exception as e:
        print(f"Erreur dans Message_Text_input_callback : {e}")


if __name__ == "__main__":
    # Initialisation de l'agent
    agent = Whiteboard(agent_name="Whiteboard", device="Wi-Fi", port=5670)
    is_interrupted = False
 

    # Ajout d'une image et d'une forme au tableau blanc
    agent.add_image(
        "https://raw.githubusercontent.com/acromtech/Voice_Driven_Humanoid_Head/main/software/pic/anim1.png",
        75.0,
        105.0,
    )
    agent.add_shape("ellipse", 177.0, 15.0, 50.0, 50.0, "red", 0.0, 0.0)

    # Boucle principale pour envoyer des messages
    cpt = 1
    while (not is_interrupted) and igs.is_started():  # Utilisation d'une méthode pour vérifier si le service doit s'arrêter
        if cpt == 1:
            agent.chat("Bonjour, j'aurais besoin d'aide.")
            cpt = 2
        elif cpt == 2:
            agent.chat("Merci !")
            cpt = 1

        time.sleep(5)  # Pause pour simuler un délai
