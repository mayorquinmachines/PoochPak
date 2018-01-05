# Project: PoochPak 

* Home security systems may be vulnerable where stationary webcam coverage is weak.
* Access to real-time GPS data may help retrieve a lost pet.
* K9 Rescue and Security operations may benefit from object recognition algorithms or environmental sensors.

Deploy your own furry minions! The PoochPak leverages the special abilities/perspective of dogs for a 'poochies-in-the-loop' system to collect and execute logic based on audio/visual and biometric cues.

![](https://s3-us-west-2.amazonaws.com/mayorquinmachines.ai/images/poochpak_walking.gif)

## Hardware
* Raspberry Pi
* Hologram Nova USB Modem
* PNY PowerPack
* Infrared Night Vision Camera
* Pulse Sensor
* Temperature Sensor

## Software
Requirements:
- [Raspbian image 2017-06-21 for Pi 3](http://downloads.raspberrypi.org/raspbian/images/raspbian-2017-06-23/2017-06-21-raspbian-jessie.zip)
- [OpenCV for Pi Zero](https://www.pyimagesearch.com/2015/12/14/installing-opencv-on-your-raspberry-pi-zero/) or [OpenCV for Pi 3](https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/)
- Apache2 server
- [Tensorflow for Pi Zero](https://petewarden.com/2017/08/20/cross-compiling-tensorflow-for-the-raspberry-pi/) or [Tensorflow for Pi 3](https://github.com/samjabrahams/tensorflow-on-raspberry-pi)
- Numpy
- [Keras2](https://nikhilraghava.wordpress.com/2017/08/05/installing-keras-on-raspberry-pi-3/)
- [hologram-python-sdk](https://github.com/hologram-io/hologram-python)
- [YOLO on Raspian](https://github.com/PiSimo/PiCamNN)

### A Note on Raspbian:
Compatibility between project dependencies requires python3.4 as default python3. I DO NOT recommend changing default python3 version, you should burn this specific image for your raspberry pi:
http://downloads.raspberrypi.org/raspbian/images/raspbian-2017-06-23/2017-06-21-raspbian-jessie.zip

#### Enable Pi camera command
```sudo modprobe bcm2835-v4l2```

#### Setting up Hologram
``` git clone https://github.com/hologram-io/hologram-python 
cd hologram-python 
sudo pip -r requirements.txt 
sudo python setup.py install
```

#### Starting YOLO object recognition
``` 
cd yolo_picam/
nohup sudo python3 picam.py &
```

#### Starting Server
``` 
nohup sudo python poochpak_server.py &
```

### Wiring the Sensors
![Wiring](http://mayorquinmachines.ai/images/poochpak_bb.png)
