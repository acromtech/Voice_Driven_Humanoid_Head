import ingescape as igs
import time


class Whiteboard:
    def __init__(self, agent_name="Whiteboard", device="Wi-Fi", port=5670):
        """Initialisation de l'agent et des configurations de base."""
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

        # Liste des URLs des GIFs
        self.gif_urls = [
            "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExc2hmc3czZnNpcG1rZTlzdW84MGJlejBhd3Y4eTN6MzBmMDl1N3JsbSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/qXJMjb6HfXG7AFyBTR/giphy.gif",
            "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExc2hmc3czZnNpcG1rZTlzdW84MGJlejBhd3Y4eTN6MzBmMDl1N3JsbSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/qXJMjb6HfXG7AFyBTR/giphy.gif",
            "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNjUwdWcxb2Y4b2EyMGF4Nmc4bXFwaWkyaGh0NmVsejF6cm1xZXV5ZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/4UTrdaK7vh0ySB7EUm/giphy.gif",
            "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNjUwdWcxb2Y4b2EyMGF4Nmc4bXFwaWkyaGh0NmVsejF6cm1xZXV5ZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/4UTrdaK7vh0ySB7EUm/giphy.gif",
            "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZm94dzh1MWo2emV0dDN6MTF6enNxcDF1ZWhwNXkzZDJsaGpwY2Q5NiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/YmN6he2EO2JHfOPiZ1/giphy.gif",
            "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZm94dzh1MWo2emV0dDN6MTF6enNxcDF1ZWhwNXkzZDJsaGpwY2Q5NiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/YmN6he2EO2JHfOPiZ1/giphy.gif",
        ]

        # Démarrage de l'agent
        igs.start_with_device(self.device, self.port)
        time.sleep(2)  # Pause pour s'assurer que le service démarre correctement

    def add_image(self, image_url, x, y, width, height):
        """Ajoute une image sur le tableau blanc."""
        self.cpt = self.cpt + 2
        igs.service_call("Whiteboard", "addImageFromUrl", (image_url, x, y, width, height), "")

    def chat(self, message_text):
        """Envoie un message sur le tableau blanc."""
        igs.service_call("Whiteboard", "chat", message_text, "")

    def clear(self):
        """Efface le contenu du tableau blanc."""
        
        for i in range(self.cpt):  # 6 est le nombre d'éléments à supprimer, vous pouvez ajuster ce nombre
            igs.service_call("Whiteboard", "remove", i, "")
        
    
    def gif_choice(self, answer_eyes):
        if answer_eyes == "coeur":
            selected_gifs = self.gif_urls[0:2]
        elif answer_eyes == "etoile":
            selected_gifs = self.gif_urls[2:4]
        elif answer_eyes == "singe":
            selected_gifs = self.gif_urls[4:6]
        else:
            print("Choix invalide")
            selected_gifs = []
            

        # Calcul pour centrer les GIFs
        if selected_gifs:
            total_gifs_width = 2 * self.gif_width  # Largeur totale des deux GIFs côte à côte
            start_x = (self.total_width - total_gifs_width) / 2  # Position x pour le premier GIF
            center_y = (self.total_height - self.gif_height) / 2  # Position y pour centrer les GIFs verticalement

            # Ajout des deux GIFs
            for i, gif_url in enumerate(selected_gifs):
                x = start_x + i * self.gif_width  # Position horizontale du GIF
                self.add_image(gif_url, x, center_y, self.gif_width, self.gif_height)




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
    
    while True:
        # Demander le choix de l'utilisateur
        answer_eyes = (input("Entrez 1 pour la ligne 1, 2 pour la ligne 2, ou 3 pour la ligne 3 : "))
        agent.clear()
        agent.gif_choice(answer_eyes)
        
        