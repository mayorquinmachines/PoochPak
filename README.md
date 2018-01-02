# Pooch Pak Project

* Home security systems may be vulnerable where stationary webcam coverage is weak.
* Access to real-time GPS data may help retrieve a lost pet.
* K9 Rescue and Security operations may benefit from object recognition algorithms or environmental sensors.

The PoochPak leverages the special abilities/perspective of dogs for a 'poochies-in-the-loop' system to collect and execute logic based on audio/visual and biometric cues.

## Hardware
* Raspberry Pi
* Hologram Nova USB Modem
* PNY PowerPack
* Infrared Night Vision Camera
* Pulse Sensor
* Temperature Sensor

## Software
Requirements:
- Raspian image 2017-06-21
- OpenCV for Python3
- Apache2 server
- Tensorflow for Raspbian
- Numpy
- Keras2
- [hologram-python-sdk](https://github.com/hologram-io/hologram-python)
- [YOLO on Raspian](https://github.com/PiSimo/PiCamNN)

## Rasbian Jessie
For this project, python3.4 is required as the main python3 version used for all installations. Unless you want to
install python3.4 yourself (I highly DO NOT recommend this), you should burn this specific image for your raspberry pi:
http://downloads.raspberrypi.org/raspbian/images/raspbian-2017-06-23/2017-06-21-raspbian-jessie.zip

** Enable Pi camera command **
``` sudo modprobe bcm2835-v4l2 ```

** Setting up Hologram **
``` git clone https://github.com/hologram-io/hologram-python 
cd hologram-python 
sudo pip -r requirements.txt 
sudo python setup.py install ```

