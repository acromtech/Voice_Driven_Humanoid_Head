import ctypes
import os
import time

def service_callback(sender_agent_name, sender_agent_uuid, service_name, arguments, token, my_data):
    pass
    # add code here if needed
    
class RobotHead:
    def __init__(self, agent_name="RobotHead", device="Wi-Fi", port=5670, simulation_mode=True):
        """Initialisation de l'agent et des configurations de base."""
        if simulation_mode == False:
            # Charger les bibliothèques nécessaires
            ctypes.CDLL("libsystemd.so", mode=ctypes.RTLD_GLOBAL)
            ctypes.CDLL("libuuid.so", mode=ctypes.RTLD_GLOBAL)
        import ingescape as igs
        self.igs = igs

        self.agent_name = agent_name
        self.device = device
        self.port = port
        self.cpt = 0

        # Configuration de l'agent
        self.igs.agent_set_name(self.agent_name)
        """
        self.igs.definition_set_class("RobotHead")
        self.igs.log_set_console(True)
        self.igs.log_set_file(True, None)
        self.igs.service_init("add_image", service_callback, None)
        self.igs.service_arg_add("add_image", "image_path", igs.STRING_T)
        self.igs.service_arg_add("add_image", "x", igs.INTEGER_T)
        self.igs.service_arg_add("add_image", "y", igs.INTEGER_T)
        self.igs.service_arg_add("add_image", "width", igs.INTEGER_T)
        self.igs.service_arg_add("add_image", "height", igs.INTEGER_T)
        self.igs.service_init("chat", service_callback, None)
        self.igs.service_arg_add("chat", "message_text", igs.STRING_T)
        self.igs.service_init("clear", service_callback, None)
        self.igs.service_init("clear_all", service_callback, None)
        self.igs.service_init("gif_choice", service_callback, None)
        self.igs.service_arg_add("gif_choice", "answer_eyes", igs.STRING_T)
        self.igs.service_init("stop", service_callback, None)
	"""
        # Disposition du tableau (3 colonnes, 2 lignes)
        self.grid_columns = 3
        self.grid_rows = 2
        self.total_width = 800
        self.total_height = 600

        # Hauteur de chaque ligne (ligne 1 plus petite)
        self.cell_height_line1 = self.total_height * 0.4  # 33% de la hauteur totale
        self.cell_height_line2 = self.total_height * 0.6  # 67% de la hauteur totale

        # Largeur de chaque colonne
        self.cell_width = self.total_width / self.grid_columns
        self.gif_width = self.cell_width * 0.9
        self.gif_height_line1 = self.cell_height_line1 * 0.9
        self.gif_height_line2 = self.cell_height_line2 * 0.9

        # Chemin absolu basé sur le répertoire courant et le sous-dossier 'pic'
        base_path = os.getcwd()

        # Vérifie si "/lib" est déjà dans le chemin
        if "/lib" not in base_path:
            base_path = os.path.join(base_path, "lib")

        # Construction du chemin vers le dossier "pic"
        pic_path = os.path.join(base_path, "pic")
        pic_path = f"file:///{pic_path}"

        # Liste des chemins absolus des GIFs
        self.gif_paths = [
            os.path.join(pic_path, "love.gif"),  # Coeur GIF 1
            os.path.join(pic_path, "love.gif"),  # Coeur GIF 2
            os.path.join(pic_path, "star.gif"),  # Etoile GIF 1
            os.path.join(pic_path, "star.gif"),  # Etoile GIF 2
            os.path.join(pic_path, "monkey.gif"),  # Singe GIF 1
            os.path.join(pic_path, "monkey.gif"),  # Singe GIF 2
            os.path.join(pic_path, "mouth2.gif"),  # Mouth GIF
            os.path.join(pic_path, "mouth3.png"),  # Mouth IMAGE PNG
            os.path.join(pic_path, "neutre.gif")  # Mouth GIF
        ]

        # Démarrage de l'agent
        self.igs.start_with_device(self.device, self.port)
        time.sleep(2)  # Pause pour s'assurer que le service démarre correctement

    def add_image(self, image_path, x, y, width, height):
        """Ajoute une image sur le tableau blanc."""
        self.cpt = self.cpt + 1
        self.igs.service_call("Whiteboard", "addImageFromUrl", (image_path, x, y, width, height), "")

    def chat(self, message_text):
        """Envoie un message sur le tableau blanc."""
        self.igs.service_call("Whiteboard", "chat", message_text, "")

    def clear(self):
        """Efface le contenu du tableau blanc."""
        for i in range(self.cpt):
            self.igs.service_call("Whiteboard", "remove", i, "")

    def clear_all(self):
        """Efface le contenu du Whiteboard et du chat"""
        self.igs.service_call("Whiteboard", "clear", None, "")

    def gif_choice(self, answer_eyes, answer_mouth):
        """Affiche des GIFs en fonction de la sélection de l'utilisateur (yeux + bouche)."""

        # Vérification du choix de l'utilisateur pour les yeux
        if answer_eyes == "amoureux":
            selected_gifs_eyes = self.gif_paths[0:2]  # Coeurs
        elif answer_eyes == "heureux":
            selected_gifs_eyes = self.gif_paths[2:4]  # Etoiles
        elif answer_eyes == "animal":
            selected_gifs_eyes = self.gif_paths[4:6]  # Singe
        else:
            selected_gifs_eyes = [self.gif_paths[8]]

        if answer_mouth == "big_smile":
            mouth_gif = self.gif_paths[6]
        else:
            mouth_gif = self.gif_paths[7]

        # Positions horizontales
        start_x_eyes_left = self.cell_width * 0.1  # Colonne 1
        start_x_eyes_right = self.cell_width * 1.9  # Colonne 3
        start_x_mouth = self.cell_width  # Colonne 2

        # Position verticale ajustée
        start_y_eyes = self.cell_height_line1 * 0.1  # Les yeux restent en haut
        start_y_mouth = self.cell_height_line1 + (self.cell_height_line2 * 0.2)  # BOUCHE PLUS HAUT

        # Placer les GIFs des yeux
        self.add_image(selected_gifs_eyes[0], start_x_eyes_left, start_y_eyes, self.gif_width, self.gif_height_line1)
        self.add_image(selected_gifs_eyes[0], start_x_eyes_right, start_y_eyes, self.gif_width, self.gif_height_line1)

        # Placer le GIF de la bouche
        self.add_image(mouth_gif, start_x_mouth, start_y_mouth, self.gif_width, self.gif_height_line2)


    def stop(self):
        self.igs.stop()

if __name__ == "__main__":
    try:
        # Initialisation de l'agent
        #agent = RobotHead(device="Wi-Fi", simulation_mode=True) # Simulation
        agent = RobotHead(device="wlo1", simulation_mode=True) # Simulation
        #agent = RobotHead(device="wlan0", simulation_mode=False) # With RaspberryPi (RobotHead)
        while True:
        # Demander le choix de l'utilisateur
            answer_eyes = input("Entrez 'amoureux'/'heureux'/'animal' ou 'quitter': ").strip().lower()
            answer_mouth = input("Entrez 'big_smile'/'smile' ou 'quitter': ").strip().lower()
            agent.clear()
            agent.gif_choice(answer_eyes, answer_mouth)
            if answer_eyes == 'quitter':
                agent.clear_all()
                break
    finally:
        pass
