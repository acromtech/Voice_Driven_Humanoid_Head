# Waveshare 1.28inch LCD Module animated eyes powered by RaspberryPi 3B+

**Ubuntu Server 22.10 (32bit) on RaspberryPi 3B+**

You can check the steps on [raspberrypi-france.fr](https://www.raspberrypi-france.fr/lancer-un-script-python-au-demarrage-du-raspberry-pi/) to launch the soft automaticly when Raspberry Pi started.

**Basic information**

You can easly run the program with the command below :

```
sudo python3 animatedEyes.py
```

**Pin connection**

```
EPD  	=>	RPI(BCM)
VCC    	->    	5V
GND    	->    	GND
DIN    	->    	10(SPI0_MOSI)
CLK    	->    	11(SPI0_SCK)
CS     	->    	8(CE0)
DC     	->    	25
RST    	->    	27
BL  	->    	18
```

**Installation library**

```
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3-pil
sudo apt-get install python3-numpy
sudo pip3 install RPi.GPIO
```
