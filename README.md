# Humanoid Robot Head with Real-Time Voice Interaction Using Ingescape

## Generality

This project is part of a distributed interaction course at UPSSITECH. It aims to integrate Ingescape into a physical voice interface for a humanoid robot head. The head is designed in SolidWorks, and the mechanical components are being 3D printed.

**Key Features:**
- **Voice Interaction**: The robot head can respond to vocal commands and questions, utilizing real-time speech recognition and transcription.
- **Dynamic Eye and Head Movements**: The system automatically triggers Python functions to animate the robot's eyes (using two circular RGB LCD screens) and perform head movements (using three brushless servomotors with CAN communication for 3 degrees of freedom).
- **Real-Time Transcription with Whisper**: Leveraging OpenAI's Whisper for real-time audio transcription, enabling smoother interaction between the user and the robot.
- **Hardware Setup**:
  - Raspberry Pi running Ubuntu 22.04
  - Two circular RGB LCD screens for animated eyes
  - Three MyActuator RMD-L-5005 brushless servomotors for head movement
  - USB microphone for audio input
  - Jack speaker for sound output

The goal of the project is to create an interactive platform that combines visual feedback (eye animations) and voice interactions to enhance human-robot interaction.

## Ingescape Installation on Ubuntu 22.04

1. **Download Ingescape Circle**:
   - Go to the following link: https://ingescape.com/upssitech
   - Navigate to the `Circle > linux64` directory and download the `.run` file: `Ingescape-Circle-4.0.0-131-installer-linux64.run`

2. **Install Ingescape Circle**:
   - Open a terminal and navigate to the directory where you downloaded the `.run` file.
   - Make the installer executable:
     ```bash
     chmod +x Ingescape-Circle-4.0.0-131-installer-linux64.run
     ```
   - Run the installer:
     ```bash
     ./Ingescape-Circle-4.0.0-131-installer-linux64.run
     ```
   - Follow the on-screen instructions to complete the installation.

3. **Download and Install Whiteboard**:
   - Go back to the parent directory on the website and navigate to `Whiteboard > linux`.
   - Download the `.deb` file: `whiteboard-1.0.1_0-amd64.deb`.
   - Install the `.deb` package using the following command:
     ```bash
     sudo dpkg -i whiteboard-1.0.1_0-amd64.deb
     ```
   - If there are dependency issues, resolve them by running:
     ```bash
     sudo apt-get install -f
     ```

4. **Launch Ingescape**:
   - Open a terminal and navigate to the directory where the `open.sh` script is located.
   - This script will launch both Circle and Whiteboard:
     ```bash
     ./open.sh
     ```
   - Circle and Whiteboard should start automatically, provided you haven't changed the default installation path.

5. **Add License**:
   - Download the Ingescape license file: `UPSSITECH_RSI.igslicense`.
   - Open Circle and drag and drop the license file into it to activate the software.
