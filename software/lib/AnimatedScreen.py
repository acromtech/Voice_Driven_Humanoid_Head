#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import time
import logging
import threading
import spidev as SPI
from PIL import Image, ImageSequence

sys.path.append("..")
from lib import LCD_1inch28

class AnimatedScreen:
    def __init__(self, bus, device, rst, dc, bl):
        """
        Initialise un écran Waveshare 1.28".
        :param bus: Bus SPI (0 ou 1)
        :param device: Device SPI (0 ou 1 pour CS)
        :param rst: GPIO pour le reset
        :param dc: GPIO pour DC
        :param bl: GPIO pour le rétroéclairage
        """
        self.spi = SPI.SpiDev(bus, device)
        self.display = LCD_1inch28.LCD_1inch28(spi=self.spi, rst=rst, dc=dc, bl=bl)
        self.display.Init()
        self.display.clear()

    def display_img(self, pathImage, delay=0.1):
        """Affiche une image statique."""
        self.display.ShowImage(Image.open(pathImage))
        time.sleep(delay)

    def display_gif(self, gif_path, speed_multiplier=1.0):
        """
        Affiche un GIF animé sur cet écran. S'arrête si `stop_event` est déclenché.
        :param gif_path: Chemin vers le fichier GIF
        :param stop_event: Instance de `threading.Event` pour indiquer quand stopper.
        :param speed_multiplier: Multiplicateur pour ajuster la vitesse (1.0 = normal, <1 = plus rapide, >1 = plus lent).
        """
        try:
            gif = Image.open(gif_path)
            for frame in ImageSequence.Iterator(gif):
                frame = frame.resize((240, 240))  # Adapter à la résolution de l'écran
                self.display.ShowImage(frame)
                frame_duration = gif.info.get('duration', 100) / 1000.0  # En secondes
                time.sleep(frame_duration * speed_multiplier)
        except Exception as e:
            logging.error(f"Erreur lors de l'affichage du GIF : {e}")

    def gif_choice(self, answer, speed_multiplier=1.0):
        base_path = os.getcwd()
        if "/lib" not in base_path:
            base_path = os.path.join(base_path, "lib")
        pic_path = os.path.join(base_path, "pic")
        gif_path_eye = os.path.join(pic_path, "neutre.gif")
        self.display_gif(gif_path_eye, speed_multiplier)
        gif_path_mouth = os.path.join(pic_path, "mouth3.gif")
        self.display_gif(gif_path_mouth, speed_multiplier)
        
        if answer == "amoureux":
            gif_path = os.path.join(pic_path, "love.gif")
            self.display_gif(gif_path, speed_multiplier)
            gif_path_bouche = os.path.join(pic_path, "mouth2.gif")
            self.display_gif(gif_path_bouche, speed_multiplier)
        elif answer == "heureux":
            gif_path = os.path.join(pic_path, "star.gif")
            self.display_gif(gif_path, speed_multiplier)
            gif_path_bouche = os.path.join(pic_path, "mouth2.gif")
            self.display_gif(gif_path_bouche, speed_multiplier)
        elif answer == "animal":
            gif_path = os.path.join(pic_path, "monkey.gif")
            self.display_gif(gif_path, speed_multiplier)
            gif_path_bouche = os.path.join(pic_path, "mouth2.gif")
            self.display_gif(gif_path_bouche, speed_multiplier)
        else:
            print("No animation specified for this case")

    def clear(self):
        """Nettoie l'écran."""
        self.display.clear()

# Fonction pour animer un écran dans un thread
def animate_screen(screen, gif_path, speed_multiplier):
    screen.display_gif(gif_path, speed_multiplier)

if __name__ == "__main__":
    # GPIO and SPI pin configuration
    # Left and right eyes (sharing SPI0 with different chip selects)
    bus_eyes = 0
    rst_eye_left = 27
    dc_eye_left = 25
    bl_eye_left = 23
    device_eye_left = 0

    # Mouth (SPI1)
    bus_mouth = 1
    rst_mouth = 5
    dc_mouth = 19
    bl_mouth = 6
    device_mouth = 0

    # Initialize the screens
    eye_left = AnimatedScreen(bus_eyes, device_eye_left, rst_eye_left, dc_eye_left, bl_eye_left)
    mouth = AnimatedScreen(bus_mouth, device_mouth, rst_mouth, dc_mouth, bl_mouth)

    # Paths to GIFs
    gif_eye_left = './pic/load1.gif'
    gif_mouth = './pic/load3.gif'

    # Speed multipliers (1.0 = normal speed, >1 = slower, <1 = faster)
    speed_eye_left = 0.01
    speed_mouth = 0.01

    # Launch animations in separate threads
    try:
        thread_eye_left = threading.Thread(target=animate_screen, args=(eye_left, gif_eye_left, speed_eye_left))
        thread_mouth = threading.Thread(target=animate_screen, args=(mouth, gif_mouth, speed_mouth))

        thread_eye_left.start()
        thread_mouth.start()

        input("Animations are running. Press Enter to stop...")

        # Wait for threads to finish
        thread_eye_left.join()
        thread_mouth.join()

    except KeyboardInterrupt:
        logging.info("Program interrupted.")
    finally:
        # Clear screens before exiting
        eye_left.clear()
        mouth.clear()
        logging.info("Program stopped.")

