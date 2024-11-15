from speech_synthesis import SyntheseVocale
import ingescape as igs
import time

class Decision:
    def __init__(self):
        # Dictionnaire de réponses basées sur le message de la transcription
        self.responses = {
            "bonjour": {
                "answer_text": "Bonjour, comment puis-je vous aider ?",
                "answer_move": "head_nod",  # Exemple de mouvement
                "answer_eyes": "blink_fast"  # Exemple d'animation des yeux
            },
            "aide": {
                "answer_text": "Je suis là pour vous aider. De quoi avez-vous besoin ?",
                "answer_move": "head_tilt_left",
                "answer_eyes": "look_left"
            },
            "merci": {
                "answer_text": "De rien ! Si vous avez d'autres questions, n'hésitez pas.",
                "answer_move": "head_nod",
                "answer_eyes": "smile"
            },
            # Ajoutez d'autres mots clés et leurs réponses correspondantes ici
        }

    def get_response(self, message_text):
        """Retourne la réponse correspondante au message de transcription."""
        # On normalise le texte pour une meilleure correspondance
        normalized_text = message_text.lower()
        for keyword, response in self.responses.items():
            if keyword in normalized_text:
                return response["answer_text"], response["answer_move"], response["answer_eyes"]
        # Retourne une réponse par défaut si aucun mot-clé n'est trouvé
        return "Je n'ai pas compris votre demande.", "neutral_position", "neutral"

def on_agent_event_callback(event, uuid, name, event_data, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Decision)
        # add code here if needed
        
        # if event.type == igs.AGENT_KNOWS_US:
        # 	if name == "Whiteboard":
        # 		igs.service_call("Whiteboard", "clear", None, "")
        		
        # if event.type = igs.AGENT_EXITED:
        # 	igs.service_call("Whiteboard", "clear", None, "")
    except:
        print(traceback.format_exc())

def Message_Text_input_callback(io_type, name, value_type, value, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Decision)
        # add code here if needed
        # igs.output_set_string("answer_text", value);
        igs.service_call("Whiteboard", "chat", "hello", "")
    except:
        print(traceback.format_exc())

if __name__ == "__main__":
    print("decision.py")
    port = 5670
    agent_name = "Decision"
    device = "wlo1"
    verbose = False
    is_interrupted = False
    agent = Decision()
    cpt = 1
    igs.agent_set_name(agent_name)
    igs.observe_agent_events(on_agent_event_callback, agent)
    igs.input_create("message_text", igs.STRING_T, None)
    igs.output_create("answer_text", igs.STRING_T, None)
    igs.output_create("answer_move", igs.STRING_T, None)
    igs.output_create("answer_eyes", igs.STRING_T, None)
    igs.observe_input("message_text", Message_Text_input_callback, agent)
    igs.start_with_device(device, port)
    time.sleep(2)
    igs.service_call("Whiteboard", "addImageFromUrl", ("file:////home/alexis/interaction distribuee/software/droite_clin_oeil.png", 75.0, 105.0), "")
    igs.service_call("Whiteboard", "addShape", ("ellipse", 177.0, 15.0, 50.0, 50.0, "red", 0.0, 0.0), "")
    
    synthese_vocale = SyntheseVocale()
    
    while (not is_interrupted) and igs.is_started():
    
        # Exemple de message de transcription
        if cpt==1 : 
            message_text = "Bonjour, j'aurais besoin d'aide."
            igs.service_call("Whiteboard", "chat", message_text, "")
            cpt=2
            
        if cpt==2 : 
            message_text = "Merci !"
            igs.service_call("Whiteboard", "chat", message_text, "")
            cpt=1
        
        # Obtenez la réponse personnalisée
        answer_text, answer_move, answer_eyes = agent.get_response(message_text)

        # Affichage des réponses
        print(f"Réponse : {answer_text}")
        print(f"Mouvement : {answer_move}")
        print(f"Yeux : {answer_eyes}")

        # Jouer la réponse audio
        synthese_vocale.generate_audio('fr', answer_text)
        time.sleep(2)
        
        print("Test de synthèse vocale terminé.")

