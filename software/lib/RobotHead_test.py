#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

import ctypes
import os
import time
import ingescape as igs

# Callback pour les inputs
def Message_Text_input_callback(io_type, name, value_type, value, my_data):
    """Callback pour la réception de messages."""
    try:
        agent_object = my_data
        assert isinstance(agent_object, RobotHead)
        agent_object.chat("hello")
    except Exception as e:
        print(f"Erreur dans Message_Text_input_callback : {e}")


class RobotHead(igs.Agent):
    def __init__(self, agent_name="RobotHead", device="Wi-Fi", port=5670, simulation_mode=True):
        super().__init__(agent_name, True)

        # Initialisation des attributs personnalisés
        self.device = device
        self.port = port
        self.cpt = 0
        self.grid_columns = 3
        self.grid_rows = 2
        self.total_width = 800
        self.total_height = 600
        self.cell_height_line1 = self.total_height * 0.33
        self.cell_height_line2 = self.total_height * 0.67
        self.cell_width = self.total_width / self.grid_columns
        self.gif_width = self.cell_width * 0.9
        self.gif_height_line1 = self.cell_height_line1 * 0.9
        self.gif_height_line2 = self.cell_height_line2 * 0.9

        base_path = os.getcwd()
        pic_path = os.path.join(base_path, "lib/pic" if not __name__ == "__main__" else "pic")
        self.gif_paths = [
            os.path.join(f"file:///{pic_path}", "love.gif"),
            os.path.join(f"file:///{pic_path}", "love.gif"),
            os.path.join(f"file:///{pic_path}", "star.gif"),
            os.path.join(f"file:///{pic_path}", "star.gif"),
            os.path.join(f"file:///{pic_path}", "monkey.gif"),
            os.path.join(f"file:///{pic_path}", "monkey.gif"),
            os.path.join(f"file:///{pic_path}", "monkey.gif")
        ]

        # Configuration des services
        self.service_init("add_image", Add_Image_callback, self)
        self.service_arg_add("add_image", "image_path", igs.STRING_T)
        self.service_arg_add("add_image", "x", igs.INTEGER_T)
        self.service_arg_add("add_image", "y", igs.INTEGER_T)
        self.service_arg_add("add_image", "width", igs.INTEGER_T)
        self.service_arg_add("add_image", "height", igs.INTEGER_T)

        self.service_init("chat", Chat_callback, self)
        self.service_arg_add("chat", "message_text", igs.STRING_T)

        self.service_init("clear", Clear_callback, self)

        self.service_init("gif_choice", Gif_Choice_callback, self)
        self.service_arg_add("gif_choice", "answer_eyes", igs.STRING_T)

        self.service_init("stop", Stop_callback, self)

        # Lancer l'agent
        if not simulation_mode:
            ctypes.CDLL("libsystemd.so", mode=ctypes.RTLD_GLOBAL)
            ctypes.CDLL("libuuid.so", mode=ctypes.RTLD_GLOBAL)
        self.start_with_device(self.device, self.port)
        time.sleep(2)

    def Add_Image(self, sender_agent_name, sender_agent_uuid, image_path, x, y, width, height):
        """Ajoute une image sur le tableau."""
        self.cpt += 2
        self.igs.service_call("Whiteboard", "addImageFromUrl", (image_path, x, y, width, height), "")

    def Chat(self, sender_agent_name, sender_agent_uuid, message_text):
        """Envoie un message."""
        self.igs.service_call("Whiteboard", "chat", message_text, "")

    def Clear(self, sender_agent_name, sender_agent_uuid):
        """Efface le contenu."""
        for i in range(self.cpt):
            self.igs.service_call("Whiteboard", "remove", i, "")

    def Gif_Choice(self, sender_agent_name, sender_agent_uuid, answer_eyes):
        """Affiche les GIFs selon la sélection."""
        selected_gifs_eyes = {
            "coeur": self.gif_paths[0:2],
            "etoile": self.gif_paths[2:4],
            "singe": self.gif_paths[4:6]
        }.get(answer_eyes, [])

        mouth_gif = self.gif_paths[6]
        start_x_eyes_left = self.cell_width * 0.1
        start_x_eyes_right = self.cell_width * 1.9
        start_x_mouth = self.cell_width
        start_y_eyes = self.cell_height_line1 * 0.1
        start_y_mouth = self.cell_height_line1 + (self.cell_height_line2 * 0.2)

        if selected_gifs_eyes:
            self.Add_Image(None, None, selected_gifs_eyes[0], start_x_eyes_left, start_y_eyes, self.gif_width, self.gif_height_line1)
            self.Add_Image(None, None, selected_gifs_eyes[1], start_x_eyes_right, start_y_eyes, self.gif_width, self.gif_height_line1)

        self.Add_Image(None, None, mouth_gif, start_x_mouth, start_y_mouth, self.gif_width, self.gif_height_line2)

    def Stop(self, sender_agent_name, sender_agent_uuid):
        """Stoppe l'agent."""
        self.igs.stop()


# Définir les callbacks
def Add_Image_callback(agent, sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    agent_object = my_data
    assert isinstance(agent_object, RobotHead)
    agent_object.Add_Image(sender_agent_name, sender_agent_uuid, *tuple_args)


def Chat_callback(agent, sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    agent_object = my_data
    assert isinstance(agent_object, RobotHead)
    agent_object.Chat(sender_agent_name, sender_agent_uuid, tuple_args[0])


def Clear_callback(agent, sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    agent_object = my_data
    assert isinstance(agent_object, RobotHead)
    agent_object.Clear(sender_agent_name, sender_agent_uuid)


def Gif_Choice_callback(agent, sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    agent_object = my_data
    assert isinstance(agent_object, RobotHead)
    agent_object.Gif_Choice(sender_agent_name, sender_agent_uuid, tuple_args[0])


def Stop_callback(agent, sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    agent_object = my_data
    assert isinstance(agent_object, RobotHead)
    agent_object.Stop(sender_agent_name, sender_agent_uuid)


if __name__ == "__main__":
    try:
        #agent = RobotHead(device="Wi-Fi", simulation_mode=True)
        agent = RobotHead(device="wlan0", simulation_mode=False)
        while True:
            answer_eyes = input("Entrez 'coeur'/'etoile'/'singe' ou 'quitter': ").strip().lower()
            agent.Clear(None, None)
            agent.Gif_Choice(None, None, answer_eyes)
            if answer_eyes == 'quitter':
                break
    finally:
        agent.Stop(None, None)

