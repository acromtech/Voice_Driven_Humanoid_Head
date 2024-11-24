import ctypes
import os
import time

class Whiteboard:
    def __init__(self, agent_name="RobotHead", device="wlan0", port=5670, simulation_mode=True):
        """Initialisation de l'agent et des configurations de base."""
        if simulation_mode == False:
            # Charger les bibliothèques nécessaires
            ctypes.CDLL("libsystemd.so", mode=ctypes.RTLD_GLOBAL)
            ctypes.CDLL("libuuid.so", mode=ctypes.RTLD_GLOBAL)
	    import ingescape as igs

        self.agent_name = agent_name
        self.device = device
        self.port = port
        self.cpt = 0

        # Configuration de l'agent
        igs.agent_set_name(self.agent_name)

        # Observation des inputs
        igs.observe_input("message_text", Message_Text_input_callback, self)

        self.grid_columns = 2
        self.total_width = 800  # Largeur totale disponible
        self.total_height = 600  # Hauteur totale disponible
        self.cell_width = self.total_width / self.grid_columns
        self.cell_height = self.total_height / 3  # 3 lignes uniquement
        self.gif_width = self.cell_width * 0.9  # Réduction pour espacement
        self.gif_height = self.cell_height * 0.9

        # Chemin absolu basé sur le répertoire courant et le sous-dossier 'pic'
        base_path = os.getcwd()
        if __name__ == "__main__":
            pic_path = os.path.join(base_path, "pic")
        else: 
            pic_path = os.path.join(base_path, "lib/pic")
        pic_path = f"file:///{pic_path}"

        # Liste des chemins absolus des GIFs
        self.gif_paths = [
            os.path.join(pic_path, "love.gif"),
            os.path.join(pic_path, "love.gif"),
            os.path.join(pic_path, "star.gif"),
            os.path.join(pic_path, "star.gif"),
            os.path.join(pic_path, "monkey.gif"),
            os.path.join(pic_path, "monkey.gif"),
        ]

        # Démarrage de l'agent
        igs.start_with_device(self.device, self.port)
        time.sleep(2)  # Pause pour s'assurer que le service démarre correctement

    def add_image(self, image_path, x, y, width, height):
        """Ajoute une image sur le tableau blanc."""
        self.cpt = self.cpt + 2
        igs.service_call("Whiteboard", "addImageFromUrl", (image_path, x, y, width, height), "")

    def chat(self, message_text):
        """Envoie un message sur le tableau blanc."""
        igs.service_call("Whiteboard", "chat", message_text, "")

    def clear(self):
        """Efface le contenu du tableau blanc."""
        for i in range(self.cpt):
            igs.service_call("Whiteboard", "remove", i, "")

    def gif_choice(self, answer_eyes):
        """Affiche des GIFs en fonction de la sélection de l'utilisateur."""
        if answer_eyes == "coeur":
            selected_gifs = self.gif_paths[0:2]
        elif answer_eyes == "etoile":
            selected_gifs = self.gif_paths[2:4]
        elif answer_eyes == "singe":
            selected_gifs = self.gif_paths[4:6]
        else:
            print("Choix invalide")
            selected_gifs = []

        # Calcul pour centrer les GIFs
        if selected_gifs:
            total_gifs_width = 2 * self.gif_width  # Largeur totale des deux GIFs côte à côte
            start_x = (self.total_width - total_gifs_width) / 2  # Position x pour le premier GIF
            center_y = (self.total_height - self.gif_height) / 2  # Position y pour centrer les GIFs verticalement

            # Ajout des deux GIFs
            for i, gif_path in enumerate(selected_gifs):
                x = start_x + i * self.gif_width  # Position horizontale du GIF
                self.add_image(gif_path, x, center_y, self.gif_width, self.gif_height)
    def stop(self):
        igs.stop()

def Message_Text_input_callback(io_type, name, value_type, value, my_data):
    """Callback pour la réception de messages."""
    try:
        agent_object = my_data
        assert isinstance(agent_object, Whiteboard)
        agent_object.chat("hello")
    except Exception as e:
        print(f"Erreur dans Message_Text_input_callback : {e}")


if __name__ == "__main__":
    try:
        # Initialisation de l'agent
        agent = Whiteboard()

        while True:
        # Demander le choix de l'utilisateur
            answer_eyes = input("Entrez 'coeur'/'etoile'/'singe' ou 'quitter': ").strip().lower()
            agent.clear()
            agent.gif_choice(answer_eyes)
            if answer_eyes == 'quitter':
                break
    finally:
        agent.stop()
