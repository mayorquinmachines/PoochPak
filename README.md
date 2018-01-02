# Pooch Pak Project

A smart dog vest for better communication and tracking of your dog, security, and home automation.


Requirements:
- Raspian image 2017-06-21
- OpenCV for Python3
- Apache2 server
- Tensorflow for Raspbian
- Numpy
- Keras2
- hologram-python-sdk

https://github.com/PiSimo/PiCamNN

## Rasbian Jessie
For this project, python3.4 is required as the main python3 version used for all installations. Unless you want to
install python3.4 yourself (I highly DO NOT recommend this), you should burn this specific image for your raspberry pi:
http://downloads.raspberrypi.org/raspbian/images/raspbian-2017-06-23/2017-06-21-raspbian-jessie.zip

** Enable Pi camera command **
``` sudo modprobe bcm2835-v4l2 ```

** Setting up Hologram **
``` git clone https://github.com/hologram-io/hologram-python ```
``` cd hologram-python ```
``` sudo pip -r requirements.txt ```
``` sudo python setup.py install ```

