# Humanoid Robot Head with Real-Time Voice Interaction Using Ingescape

## General Overview

This project, part of a distributed interaction course at UPSSITECH, aims to integrate Ingescape into a humanoid robot head's voice interaction interface. The head, designed in SolidWorks, incorporates 3D-printed components and multiple hardware and software integrations.

### Key Features
- **Voice Interaction**: Real-time response to vocal commands and questions using speech recognition, transcription and speech synthesis with [gTTS (Google Text-To-Speech)](https://pypi.org/project/gTTS/).
- **Dynamic Eye and Head Movements**: Animated eyes on circular RGB LCD screens and head movements via [MyActuator](https://www.myactuator.com/) RMD-L-5005 Brushless Servomotors with CAN communication.
- **Real-Time Transcription with Whisper**: Integration of [OpenAI's Whisper](https://github.com/openai/whisper) for seamless audio transcription.
- **Future Development**: Facial and gesture recognition via OpenCV and MediaPipe, leveraging a [Raspberry Pi Camera Module v2 8MP](https://www.kubii.com/fr/cameras-capteurs/1653-module-camera-v2-8mp-kubii-652508442112.html).

---

## Hardware Setup
- **Core Components**:
  - 1x [Raspberry Pi 4 Model B - 8GB](https://www.kubii.com/fr/cartes-nano-ordinateurs/2955-raspberry-pi-4-modele-b-8gb-5056561800356.html?gad_source=1&gclid=Cj0KCQjwmt24BhDPARIsAJFYKk0vGSifNh3i6yDBs-2KhJvjr_JfaW2df-r5NaNHU3-WDXiL-hcrOdkaAghiEALw_wcB) (running [Ubuntu 24.04 LTS Server](https://ubuntu.com/download/server))
  - 3x [Waveshare 1.28inch Round LCD Module Displays](https://www.amazon.fr/Waveshare-1-28inch-LCD-Module-Resolution/dp/B08V5538C6/ref=sr_1_1_sspa) for animated eyes
  - 1x [Raspberry Pi Camera Module v2 8MP](https://www.kubii.com/fr/cameras-capteurs/1653-module-camera-v2-8mp-kubii-652508442112.html) for facial and gesture recognition in future iterations
  - 3x [MyActuator RMD-L-5005 brushless servomotors](https://www.myactuator.com/product-page/rmd-l-5005) for head movement
  - 1x [USB to CAN Converter](https://www.amazon.fr/Converter-Raspberry-Computer-Support-Windows/dp/B09K3LL93Q/ref=sr_1_1) for servomotor communication
  - 1x [USB 2.0 Mini Microphone](https://www.amazon.fr/dp/B01KLRBHGM?ref=ppx_yo2ov_dt_b_fed_asin_title) for audio input
  - 1x [USB Mini Speaker](https://www.kubii.com/fr/haut-parleurs-microphones/1850-mini-haut-parleurs-usb-kubii-6945379550159.html?mot_tcid=2922e452-bdf7-4af9-9242-61bf3208f7d8) for sound output

- **Mechanical Components**:
  - Design: [SolidWorks](https://www.solidworks.com/fr)
  - Slicing: [PrusaSlicer](https://www.prusa3d.com/page/prusaslicer_424/)
  - Printing: [Original Prusa MINI+](https://www.prusa3d.com/fr/produit/original-prusa-mini-semi-assemblee-4/) (180 x 180 x 180 mm volume)
  - Materials: PETG filaments ([Polymaker PolyLite PETG Black & Grey](https://www.makershop.fr/filament-3d/5050-polylite-petg-polymaker.html))
  - Additional: [Tinted visor](https://www.amazon.fr/dp/B09DPF2PPB/ref=twister_B09HH8B2VX?_encoding=UTF8&psc=1)

---

## Software Setup
To ensure seamless installation and configuration, use the provided `setup.sh` script. This script handles all necessary installations, including Python 3.11, Ingescape, and other dependencies.

### Key Software
- **Operating System**: [Ubuntu 24.04 LTS Server](https://ubuntu.com/download/server)
- **Voice and Interaction Libraries**:
  - [Ingescape](https://ingescape.com/upssitech) (Circle & Whiteboard)
  - [OpenAI's Whisper](https://github.com/openai/whisper)
- **Python Version**:
  - [Python 3.11](https://www.python.org/downloads/release/python-3110/)

---
## How It Works

The robot head is controlled by a Python-based system that listens to user input (voice commands) and responds with dynamic actions. The core functionalities are:

1. **Voice Interaction**:
    - **Whisper** is used to transcribe speech in real-time.
    - **gTTS** is used to generate speech responses from text.

2. **Dynamic Eye and Head Movements**:
    - Eye animations are shown using **Waveshare LCD displays**.
    - Head movements are controlled by **MyActuator servos**, providing realistic motions such as head tilts and nods.

3. **Decision-Making Class**:
    - The **Decision** class, using pre-programmed responses (e.g., greetings, commands), decides how the robot should respond based on the input.
    - The `get_response` function processes the message, checks for greetings and keywords, and updates the robot’s movements and facial expressions accordingly.

4. **Future Enhancements**:
    - Facial and gesture recognition using **OpenCV** and **MediaPipe**.
    - Integration of the **Raspberry Pi Camera** for improved interaction.

---

## Project Goals

The main goals of this project are:

- **Real-time voice interaction**: Provide a smooth, conversational interaction with the robot using voice commands.
- **Dynamic feedback**: Display visual feedback through dynamic eye movements and animated facial expressions.
- **Extendable platform**: Build a foundation for further features like facial recognition, gesture tracking, and more complex interactions.

---

## Project Goals
The primary objective is to create an interactive platform combining:
1. **Visual Feedback**: Eye animations through dynamic displays.
2. **Voice Interaction**: Real-time transcription and response.
3. **Future Enhancements**: Facial and gesture recognition to deepen human-robot interaction.

For installation and setup, please refer to the [setup.sh](./setup.sh) script. Follow its execution steps to prepare your environment.
