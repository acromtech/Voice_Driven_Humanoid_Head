from transcription import Transcription
from speech_synthesis import SyntheseVocale
from decision import Decision
import ingescape as igs
import time

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
        
def main():
    print("main.py")
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
    
    # Initialisation des modules
    transcripteur = Transcription()
    synthese_vocale = SyntheseVocale()
    decision_module = Decision()

    while (not is_interrupted) and igs.is_started():
        # Étape 1 : Effectuer la transcription
        message_text = transcripteur.transcribe_audio()
        print(message_text)
        igs.service_call("Whiteboard", "chat", message_text, "")
        print(f"Message transcrit : {message_text}")
        
        # Étape 2 : Obtenir la réponse personnalisée
        answer_text, answer_move, answer_eyes = decision_module.get_response(message_text)
        igs.service_call("Whiteboard", "chat", answer_text, "")
        print(f"Réponse : {answer_text}")
        print(f"Mouvement : {answer_move}")
        print(f"Yeux : {answer_eyes}")

        # Étape 3 : Jouer la réponse audio
        synthese_vocale.generate_audio('fr', answer_text)
        time.sleep(2)

    print("Test de synthèse vocale terminé.")

if __name__ == "__main__":
    main()

