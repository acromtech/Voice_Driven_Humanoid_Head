# Humanoid Robot Head with Real-Time Voice Interaction Using Ingescape

## Generality

This project is part of a distributed interaction course at UPSSITECH. It aims to integrate Ingescape into a physical voice interface for a humanoid robot head. The head is designed in SolidWorks, and the mechanical components are being 3D printed.

**Key Features:**
- **Voice Interaction**: The robot head can respond to vocal commands and questions, utilizing real-time speech recognition and transcription.
- **Dynamic Eye and Head Movements**: The system automatically triggers Python functions to animate the robot's eyes (using two circular RGB LCD screens) and perform head movements (using three brushless servomotors with CAN communication for 3 degrees of freedom).
- **Real-Time Transcription with Whisper**: Leveraging [OpenAI's Whisper](https://github.com/openai/whisper) for real-time audio transcription, enabling smoother interaction between the user and the robot.
- **Hardware Setup**:
  - 1x [Raspberry Pi 4 modèle B - 8GB](https://www.kubii.com/fr/cartes-nano-ordinateurs/2955-raspberry-pi-4-modele-b-8gb-5056561800356.html?gad_source=1&gclid=Cj0KCQjwmt24BhDPARIsAJFYKk0vGSifNh3i6yDBs-2KhJvjr_JfaW2df-r5NaNHU3-WDXiL-hcrOdkaAghiEALw_wcB) running Ubuntu 22.04
  - 2x [Waveshare 1.28inch Round LCD Module Display](https://www.amazon.fr/Waveshare-1-28inch-LCD-Module-Resolution/dp/B08V5538C6/ref=sr_1_1_sspa?dib=eyJ2IjoiMSJ9.m9qtWRt8n16G1UrD6WkJMvDmOWrhEZ27Yx1HpyymqALfAE1WB4MsumnpY4OmRNuFZ9T2mzM_glRLwZfDMwU4O8_rEGV439cx1RMnCcUokkgAm0Tuh0aG_uxwH1GuhHgbzpVlY9RTLl0eh8_g2deKUgJNhXtNbzA3rnFDXqeBr6MWHcxWeOPDwrJiwcn7gjelQez6pt47hYH3KtR2rsYy3xk3v-X9X0TQNa1YVkyF-Z4OgIqaDVhyr35QblG-ES4IYwalRugiQZi8iHKfxpXnuwyGwkwHraYydnoSuaa_2PY.TEYJs_DHyVguZJ77x_nwYbEda7ZGUwW6cDwPTf_Wyxw&dib_tag=se&keywords=waveshare+round+display&qid=1729605033&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1) for animated eyes
  - 3x [MyActuator RMD-L-5005 brushless servomotors](https://www.myactuator.com/product-page/rmd-l-5005) for head movement
  - 1x [USB to Can Converter](https://www.amazon.fr/Converter-Raspberry-Computer-Support-Windows/dp/B09K3LL93Q/ref=sr_1_1?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=3E5MT4H6XD5O6&dib=eyJ2IjoiMSJ9.rrsIu70DLhhsqjHfVWc4JiqpDP88ctD6rIwjqztbSZq2nudWwIuwTAbxJKjqVuXxrX4vtJLcc61ngPDpUDuC4r1Ut025my2tbwoiJkvAzf-kuQhpDaBCa3BzbpjIqNaxbaOM48SjgUKLzKuh3m9xDP-PxHlyRHJaBAxsxLnhUIGWJe5tu1-PwUyH0IIkXBW2vCELpg5TQ-3R4f9gE3rxh694Wp6aZmS9waR1yYoSqGtA0250pSysu1jljcaBPPhcg8kK6mFH0PGL0MK_ND8tCGYlPors2Iia5LwKuQ-xjIc.oDfN9Yy_rk0geQuren8tuevHAKkPOqEl6_Vvc_SaxAU&dib_tag=se&keywords=usb+to+can+transceiver+innomaker&qid=1729605611&s=electronics&sprefix=usb+to+can+transceiver+innomaker%2Celectronics%2C80&sr=1-1) for communicate with the servomotors
  - 1x [USB 2.0 Mini Microphone](https://www.amazon.fr/dp/B01KLRBHGM?ref=ppx_yo2ov_dt_b_fed_asin_title) for audio input
  - 1x [USB Mini Speaker](https://www.kubii.com/fr/haut-parleurs-microphones/1850-mini-haut-parleurs-usb-kubii-6945379550159.html?mot_tcid=2922e452-bdf7-4af9-9242-61bf3208f7d8) (or this one - https://www.amazon.fr/Haut-Parleur-Fr%C3%A9quence-Ordinateur-Interface-JST-PH2-0/dp/B08QFTYB9Z/ref=sr_1_2?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=7W0U2IEFH6K7&dib=eyJ2IjoiMSJ9.Qb2kT2hTn58VtHxmmkoKBajatc1OHKfxZKoQbrX_cHX8X2FKK7jQu5xAWCkRjsKxn_1WBlwKt_axFujvpcNhTyeQoEmGdAxTcdYTr8VJSO5XTCctU5qNQyWlA2DP2a-mRcG_JBqBj8_Trsln1rNa2ISQkjqsB_3VbIh4hUZ1p5HjNJrxsBKb7s7w_SmYLOUq8V4P5GTgePphsRxDZmUueYmPzRDhU3PeZqsaFt_Qitw7zf6MF8iH6MSduh3FqaC-VZpfVGJsH7wrStncPJ871McvaPe36Wf5fIF6N9rucL0.htEj1-mSZx76iObkty8FsMnq6H-w86QMGBekXD7Ai_c&dib_tag=se&keywords=haut+parleur+raspberry+pi&qid=1729605187&sprefix=haut+parleur+raspberry+pi%2Caps%2C109&sr=8-2) for sound output
- **Mechanical Setup**
  - 1x [SolidWorks](https://www.solidworks.com/fr) for designing
  - 1x [PrusaSlicer](https://www.prusa3d.com/page/prusaslicer_424/) for slicing my `STL` files to `bgcode` (Binary GCODE) files
  - 1x 3D printer (a [Original Prusa MINI+](https://www.prusa3d.com/fr/produit/original-prusa-mini-semi-assemblee-4/) in my case with a 180 x 180 x 180 mm printing volume)
  - 1x PETG filaments ([Polymaker PolyLite PETG Black 1Kg & Grey 1Kg 1.75mm](https://www.makershop.fr/filament-3d/5050-polylite-petg-polymaker.html) in my case)
  - 1x [Tinted visor](https://www.amazon.fr/dp/B09DPF2PPB/ref=twister_B09HH8B2VX?_encoding=UTF8&psc=1)
- **Software Setup**
  - [Ubuntu 22.04](https://releases.ubuntu.com/jammy/)
  - [Ingescape (including Circle & Whiteboard)](https://ingescape.com/upssitech)
  - [OpenAI's Whisper](https://github.com/openai/whisper)
  - [Python 3.11](https://www.python.org/downloads/release/python-3110/)
    ```
    sudo apt update
    sudo apt install software-properties-common -y
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt update
    sudo apt install python3.11
    ```
  - My Custom CAN Wrapper for MyActuator Servomotors

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
