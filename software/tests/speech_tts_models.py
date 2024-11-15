from TTS.api import TTS

# Initialiser TTS
tts = TTS()

# Lister les modèles disponibles
models = tts.list_models()

# Filtrer et afficher uniquement les modèles français
french_models = [model for model in models if 'fr' in model]
print("Modèles disponibles en français :")
for model in french_models:
    print(model)

