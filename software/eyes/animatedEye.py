#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet
import os
import sys 
import time
import logging
import spidev as SPI
sys.path.append("..")
from lib import LCD_1inch28
from PIL import Image,ImageDraw,ImageFont

# Raspberry Pi pin configuration:
bus=0

RST = 27
DC = 25
BL = 18
device = 0

DELAY1 = 0.01
DELAY2 = 2

def setImgToScreen(pathImage):
    disp.ShowImage(Image.open(pathImage))
    time.sleep(DELAY1)

def openEye():
    setImgToScreen('./pic/CLEAR.png')
    setImgToScreen('./pic/anim7.png')
    setImgToScreen('./pic/anim6.png')
    setImgToScreen('./pic/anim5.png')
    setImgToScreen('./pic/anim4.png')
    setImgToScreen('./pic/anim3.png')
    setImgToScreen('./pic/anim2.png')
    setImgToScreen('./pic/anim1.png')

def closeEye():
    setImgToScreen('./pic/anim1.png')
    setImgToScreen('./pic/anim2.png')
    setImgToScreen('./pic/anim3.png')
    setImgToScreen('./pic/anim4.png')
    setImgToScreen('./pic/anim5.png')
    setImgToScreen('./pic/anim6.png')
    setImgToScreen('./pic/anim7.png')
    setImgToScreen('./pic/CLEAR.png')

try:
    disp = LCD_1inch28.LCD_1inch28() # display with hardware SPI: ''' Warning!!!Don't  creation of multiple displayer objects!!! '''
    disp.Init()  # Initialize library.
    disp.clear() # Clear display.

    while(1):
        openEye()
        time.sleep(DELAY2)
        closeEye()

    disp.module_exit()
    logging.info("quit:")
except IOError as e:
    logging.info(e)    
except KeyboardInterrupt:
    disp.module_exit()
    logging.info("quit:")
    exit()
