import random
import time
import re
if __name__ == "__main__":
    from RobotHead import RobotHead
else:
    from lib.RobotHead import RobotHead

class Decision:
    def __init__(self, device="Wi-Fi", simulation_mode=True):
        self.agent = RobotHead(device=device, simulation_mode=simulation_mode)
        self.responses = {
            "bonjour": {
                "answer_text": "Bonjour, comment puis-je vous aider ?",
                "answer_move": "head_nod",
                "answer_eyes": "blink_fast",
                "answer_mouth": "smile"
            },
            "aide": {
                "answer_text": "Je suis là pour vous aider. De quoi avez-vous besoin ?",
                "answer_move": "head_tilt_left",
                "answer_eyes": "look_left",
                "answer_mouth": "smile"
            },
            "merci": {
                "answer_text": "De rien ! Si vous avez d'autres questions, n'hésitez pas.",
                "answer_move": "head_nod",
                "answer_eyes": "smile",
                "answer_mouth": "smile"
            },
            "bonjour matin": {
                "answer_text": "Bonjour, belle matinée ! Comment puis-je vous assister ce matin ?",
                "answer_move": "head_nod",
                "answer_eyes": "look_right",
                "answer_mouth": "smile"
            },
            "bonsoir": {
                "answer_text": "Bonsoir, comment puis-je vous aider ce soir ?",
                "answer_move": "head_tilt_left",
                "answer_eyes": "look_up",
                "answer_mouth": "smile"
            },
            "help": {
                "answer_text": "I am here to help. What do you need assistance with?",
                "answer_move": "head_tilt_right",
                "answer_eyes": "look_left",
                "answer_mouth": "smile"
            },
            "animal": {
                "answer_text": "Ooo Ooo Ah Ah !",
                "answer_move": "head_bob",
                "answer_eyes": "animal",
                "answer_mouth": "smile"
            },
            "amoureux": {
                "answer_text": "Je suis tellement heureux, regarde-moi !",
                "answer_move": "head_nod",
                "answer_eyes": "amoureux",
                "answer_mouth": "big_smile"
            },
            "heureux": {
                "answer_text": "Wow, c'est incroyable !",
                "answer_move": "head_tilt_back",
                "answer_eyes": "heureux",
                "answer_mouth": "open_wide"
            }
        }
        self.default_response = {
            "answer_text": "Je n'ai pas compris votre demande.",
            "answer_move": "neutral_position",
            "answer_eyes": "neutral",
            "answer_mouth": "smile"
        }
    
    def get_response(self, message_text):
        """Retourne la réponse correspondante au message de transcription."""
        self.agent.chat(message_text)
        normalized_text = message_text.lower()

        # Check for time-based greetings
        current_hour = time.localtime().tm_hour
        if current_hour < 12:
            greetings = ["bonjour", "bonjour matin"]
        else:
            greetings = ["bonsoir"]

        # Search for greetings first
        for greeting in greetings:
            if greeting in normalized_text:
                return self.responses.get(greeting, self.default_response)["answer_text"], \
                       self.responses.get(greeting, self.default_response)["answer_move"], \
                       self.responses.get(greeting, self.default_response)["answer_eyes"], \
                       self.responses.get(greeting, self.default_response)["answer_mouth"]

        # Search for other specific responses using keywords
        for keyword, response in self.responses.items():
            if re.search(r'\b' + re.escape(keyword) + r'\b', normalized_text):  # Ensure word boundaries
                self.agent.clear()
                self.agent.gif_choice(response["answer_eyes"], response["answer_mouth"])
                self.agent.chat(response["answer_text"])
                return response["answer_text"], response["answer_move"], response["answer_eyes"], response["answer_mouth"]

        # If no response is found, provide the default response
        return self.default_response["answer_text"], self.default_response["answer_move"], self.default_response["answer_eyes"], self.default_response["answer_mouth"]

    def add_response(self, keyword, answer_text, answer_move, answer_eyes, answer_mouth):
        """Permet d'ajouter une nouvelle réponse à la liste des réponses."""
        self.responses[keyword] = {
            "answer_text": answer_text,
            "answer_move": answer_move,
            "answer_eyes": answer_eyes,
            "answer_mouth": answer_mouth
        }

    def remove_response(self, keyword):
        """Permet de retirer une réponse existante."""
        if keyword in self.responses:
            del self.responses[keyword]

    def update_response(self, keyword, answer_text=None, answer_move=None, answer_eyes=None, answer_mouth=None):
        """Permet de modifier une réponse existante."""
        if keyword in self.responses:
            if answer_text:
                self.responses[keyword]["answer_text"] = answer_text
            if answer_move:
                self.responses[keyword]["answer_move"] = answer_move
            if answer_eyes:
                self.responses[keyword]["answer_eyes"] = answer_eyes
            if answer_mouth:
                self.responses[keyword]["answer_mouth"] = answer_mouth

    def reset(self):
        self.agent.clear_all()

if __name__ == "__main__":
    # Création d'un objet Decision
    # decision = Decision(device="Wi-Fi", simulation_mode=True) # SIMULATION MODE
    decision = Decision(device="wlan0", simulation_mode=False) # WITH RASPBERRY PI (ROBOT HEAD)

    # Exemple de message à tester
    test_messages = [
        "Bonjour, comment ça va ?",
        "Aide, s'il vous plaît.",
        "Merci beaucoup !",
        "Bonjour, c'est une belle matinée.",
        "Bonsoir, robot !",
        "Help me please.",
        "Quel est votre nom ?",
        "amoureux",
        "heureux",
        "animal"
    ]

    # Test des messages
    for message in test_messages:
        print(f"Message: {message}")
        text, move, eyes, mouth = decision.get_response(message)
        print("Réponse texte:", text)
        print("Mouvement:", move)
        print("Yeux:", eyes)
        print("-------------")
        input("appuyez sur entrer")
    decision.reset()
"""
    # Ajouter une nouvelle réponse et tester
    decision.add_response("salut", "Salut, comment ça va ?", "head_nod", "blink_slow")
    print("Ajout d'une nouvelle réponse 'salut'.")
    text, move, eyes, mouth = decision.get_response("Salut, robot !")
    print("Réponse texte après ajout:", text)
    print("Mouvement après ajout:", move)
    print("Yeux après ajout:", eyes)
    print("-------------")

    # Modifier une réponse existante et tester
    decision.update_response("salut", answer_text="Salut, comment ça va aujourd'hui ?", answer_move="head_tilt_right")
    print("Modification de la réponse 'salut'.")
    text, move, eyes, mouth = decision.get_response("Salut, robot !")
    print("Réponse texte après modification:", text)
    print("Mouvement après modification:", move)
    print("Yeux après modification:", eyes)
    print("-------------")

    # Supprimer une réponse et tester
    decision.remove_response("salut")
    print("Suppression de la réponse 'salut'.")
    text, move, eyes, mouth = decision.get_response("Salut, robot !")
    print("Réponse texte après suppression:", text)
    print("Mouvement après suppression:", move)
    print("Yeux après suppression:", eyes)
"""
