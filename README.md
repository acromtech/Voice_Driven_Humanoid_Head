# Humanoid Robot Head with Real-Time Voice Interaction Using Ingescape

## General Overview

This project, part of a distributed interaction course at UPSSITECH, aims to integrate Ingescape into a humanoid robot head's voice interaction interface. The head, designed in SolidWorks, incorporates 3D-printed components and multiple hardware and software integrations.

### Key Features
- **Voice Interaction**: Real-time response to vocal commands and questions using speech recognition, transcription and speech synthesis with [gTTS (Google Text-To-Speech)](https://pypi.org/project/gTTS/).
- **Dynamic Eye and Head Movements**: Animated eyes on circular RGB LCD screens and head movements via [MyActuator](https://www.myactuator.com/) RMD-L-5005 Brushless Servomotors with CAN communication.
- **Real-Time Transcription with Whisper**: Integration of [OpenAI's Whisper](https://github.com/openai/whisper) for seamless audio transcription.
- **Future Development**: Facial and gesture recognition via OpenCV and MediaPipe, leveraging a [Raspberry Pi Camera Module v2 8MP](https://www.kubii.com/fr/cameras-capteurs/1653-module-camera-v2-8mp-kubii-652508442112.html).

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
To ensure seamless installation and configuration, use the provided [setup_software.sh](./software/setup_software.sh) script. This script handles all necessary installations, including Python 3.11, Ingescape, and other dependencies.

### Key Software
- **Operating System**: [Ubuntu 24.04 LTS Server](https://ubuntu.com/download/server)
- **Voice and Interaction Libraries**:
  - [Ingescape](https://ingescape.com/upssitech) (Circle & Whiteboard)
  - [OpenAI's Whisper](https://github.com/openai/whisper)
- **Python Version**:
  - [Python 3.11](https://www.python.org/downloads/release/python-3110/)

 ## System Architecture
<img width="878" alt="image" src="https://github.com/user-attachments/assets/179a303a-4917-4b71-b2dd-fb0eb7199d7a">

## Installation
Please use the following command to install the dependencies :
```
sudo bash setup_laptop.sh
```
You can also modify all the parameters of the devices into the main.py file
```python
# CONFIG RASPBERRY PI
"""
simulation_mode = False
device = "wlan0"
playback_device_name = "UACDemoV1.0"
sample_rate = 48000
speed_factor_tts = 1.15
recording_device_name = "USB PnP Sound Device"
mic_sample_rate = 44100
silence_threshold = 0.02
silence_duration = 0.5
"""

# YOUR LAPTOP CONFIG
simulation_mode = True
device = "wlo1"
playback_device_name = "UACDemoV1.0"
sample_rate = 48000
speed_factor_tts = 1.15
recording_device_name = "USB PnP Sound Device"
mic_sample_rate = 44100
silence_threshold = 0.02
silence_duration = 0.5
```

---
## How It Works

The robot head is controlled by a Python-based system that listens to user input (voice commands) and responds with dynamic actions. The core functionalities are:

1. **Voice Interaction**:
    - **Whisper** is used to transcribe speech in real-time.
    - **gTTS** is used to generate speech responses from text.

2. **Dynamic Eye and Mouth & Head Movements**:
    - Eye and mouth animations are shown using **Waveshare LCD displays** and on the **Whiteboard** simultaneously.


    2.1. **Whiteboard Interface**: Animated Visual Feedback
        The **whiteboard** is a visual interface where animated graphics (GIFs) are displayed to represent the robot's "expressions." This interface leverages the LCD screens for a more engaging interaction experience. Key aspects include:

  - **Dynamic Eye Movements**:
          - Depending on the robot's emotional state or context, the eyes can blink, look left or right, and even display special animations (e.g., "amoureux" for love or "animal" for playful expressions).
          - The animations are displayed on **Waveshare 1.28inch Round LCD modules**, with GIFs or specific visuals representing the state.

  - **Mouth Animations**:
          - Along with eye movements, mouth visuals change to reflect emotions (e.g., smile, wide open).
          - These animations provide non-verbal feedback that complements voice responses.

   - **Integration with Decisions**:
          - The `Decision` class drives the updates on the whiteboard interface by selecting appropriate GIFs or animations based on user input and predefined responses.

        **Example Workflow**:
        - If the user says, "heureux," the robot's eyes will display the "star" GIF, and the mouth will show a "moving mouth."
          <img width="959" alt="image" src="https://github.com/user-attachments/assets/b47c1adb-7715-4e2c-89aa-2d8919faf96f">





  2.2. **Chat Interface**: Voice Interaction and Transcription
        The **chat interface** provides real-time transcription of user speech and displays the robot's textual responses. It simulates a conversation log, making it easy for users to follow the interaction. Key components include:

   - **Speech Recognition**:
          - The **Whisper** model transcribes user speech into text, which is displayed in the chat.
          - Example: If the user says, *"Bonjour, robot !"*, the chat log will show:
            ```
            User: Bonjour, robot !
            ```

  - **Text-to-Speech Responses**:
          - The robot generates a voice response using **gTTS** and simultaneously displays the response text in the chat.
          - Example: If the robot responds, *"Bonjour, comment puis-je vous aider ?"*, the chat log will show:
            ```
            Robot: Bonjour, comment puis-je vous aider ?
            ```
        <img width="959" alt="image" src="https://github.com/user-attachments/assets/9446868b-976f-4ffa-b07d-e14e1ab28012">

    - **Seamless Integration with Decisions**:
          - The `Decision` class matches the transcription to a predefined response and updates both the whiteboard and chat interfaces accordingly.


4. **Decision-Making Class**:
    - The **Decision** class, using pre-programmed responses (e.g., greetings, commands), decides how the robot should respond based on the input.
    - The `get_response` function processes the message, checks for greetings and keywords, and updates the robot’s movements and facial expressions accordingly.


5. **Future Enhancements**:
    - Facial and gesture recognition using **OpenCV** and **MediaPipe**.
    - Integration of the **Raspberry Pi Camera** for improved interaction.


---

## V&V (Verification and Validation)

This section describes the testing strategy implemented to ensure proper functionality of the humanoid robot head.

### 1. Integration Testing
To perform integration testing:
- Run the [main.py](./software/main.py) script.
- Ensure to adjust the device parameter to match your hardware setup. Replace `"wlan0"` with your specific device (e.g., `"Wi-Fi"`) by modifying **line 38** in the main script:
  ```python
  decision = Decision(device="wlan0", simulation_mode=simulation_mode)

### 2. Unit Testing
For unit testing:
- Run the Python scripts for each module or file individually.
- Adjust the device configuration in the agent initialization at the start of each script. Replace `"Wi-Fi"` with your specific device (e.g., `"wlan0"`) as follows:
  ```python
  agent = RobotHead(device="Wi-Fi", simulation_mode=True)
  ```
### 3. Agent Testing
To evaluate the agent's performance:
- Execute the [test_robothead.igsscript](./software/test_robothead.igsscript) script: This script contains predefined scenarios to test the agent’s behavior.

---

## Project Goals

The main goals of this project are:

- **Real-time voice interaction**: Provide a smooth, conversational interaction with the robot using voice commands.
- **Dynamic feedback**: Display visual feedback through dynamic eye movements and animated facial expressions.
- **Extendable platform**: Build a foundation for further features like facial recognition, gesture tracking, and more complex interactions.

---

## Notes :

Check precommit errors : `uv run pre-commit run -a`
ssh connection RaspberryPi : `...`

For installation and setup, please refer to the [setup_software.sh](./software/setup_software.sh) script. Follow its execution steps to prepare your environment.
