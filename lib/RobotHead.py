import ctypes
import os
import time


class RobotHead:
    def __init__(
        self, agent_name="RobotHead", device="Wi-Fi", port=5670, simulation_mode=True
    ):
        """Initialisation des configurations de base."""
        if not simulation_mode:
            # Charger les bibliothèques nécessaires
            ctypes.CDLL("libsystemd.so", mode=ctypes.RTLD_GLOBAL)
            ctypes.CDLL("libuuid.so", mode=ctypes.RTLD_GLOBAL)

        self.agent_name = agent_name
        self.device = device
        self.port = port
        self.cpt = 0

        # Disposition du tableau (3 colonnes, 2 lignes)
        self.grid_columns = 3
        self.grid_rows = 2
        self.total_width = 800
        self.total_height = 600

        # Hauteur de chaque ligne (ligne 1 plus petite)
        self.cell_height_line1 = self.total_height * 0.4
        self.cell_height_line2 = self.total_height * 0.6

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
            os.path.join(pic_path, "love.gif"),
            os.path.join(pic_path, "love.gif"),
            os.path.join(pic_path, "star.gif"),
            os.path.join(pic_path, "star.gif"),
            os.path.join(pic_path, "monkey.gif"),
            os.path.join(pic_path, "monkey.gif"),
            os.path.join(pic_path, "mouth2.gif"),
            os.path.join(pic_path, "mouth3.png"),
            os.path.join(pic_path, "neutre.gif"),
        ]

    def gif_choice(self, answer_eyes, answer_mouth):
        """Affiche des GIFs en fonction de la sélection de l'utilisateur (yeux + bouche)."""

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
        start_x_eyes_left = self.cell_width * 0.1
        start_x_eyes_right = self.cell_width * 1.9
        start_x_mouth = self.cell_width

        # Position verticale ajustée
        start_y_eyes = self.cell_height_line1 * 0.1
        start_y_mouth = self.cell_height_line1 + (self.cell_height_line2 * 0.2)

        print(f"Affichage des GIFs : {selected_gifs_eyes} aux yeux, {mouth_gif} à la bouche")


if __name__ == "__main__":
    try:
        agent = RobotHead(device="wlo1", simulation_mode=True)
        while True:
            answer_eyes = (
                input("Entrez 'amoureux'/'heureux'/'animal' ou 'quitter': ")
                .strip()
                .lower()
            )
            answer_mouth = (
                input("Entrez 'big_smile'/'smile' ou 'quitter': ").strip().lower()
            )

            agent.gif_choice(answer_eyes, answer_mouth)
            if answer_eyes == "quitter":
                break
    finally:
        pass
