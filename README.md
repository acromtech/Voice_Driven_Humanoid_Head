# Humanoid Robot Head with Real-Time Voice Interaction

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

## Software Setup
To ensure seamless installation and configuration, use the provided [setup.sh](./software/setup_software.sh) script. This script handles all necessary installations.

### Key Software
- **Operating System**: [Ubuntu 20.04 LTS Server](https://ubuntu.com/download/server)
- **Python Version**: Python 3.10

### Notes
Check precommit errors : `uv run pre-commit run -a`
Check your wlan0 ip : `ip a`
ssh connection RaspberryPi : `ssh username@wlan0_ip`
