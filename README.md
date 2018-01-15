# Project: PoochPak 

* Home security systems may be vulnerable where stationary webcam coverage is weak.
* Access to real-time GPS data may help retrieve a lost pet.
* K9 Rescue and Security operations may benefit from object recognition algorithms or environmental sensors.

Deploy your own furry minions! The PoochPak leverages the special abilities/perspective of dogs for a 'poochies-in-the-loop' system to collect and execute logic based on audio/visual and biometric cues.
*Thanks to PiSimo's* [repo](https://github.com/PiSimo/PiCamNN) *for the YOLO code to run on raspbian.*

*This* [repo](https://github.com/smellslikeml/cell_pwn_drone) *is a spinoff of the same project using a drone! Check it
out!*
[Here](https://www.hackster.io/man-sbestfriend-sbesthack/poochpak-mobile-information-gathering-and-security-system-a79c58)*is a link to the contest entry on hackster.io for more info.*


![PoochPak](poochpak_walking.gif?raw=true "Pooch")

## Hardware
* [Raspberry Pi Zero](https://www.amazon.com/Raspberry-Starter-Power-Supply-Premium/dp/B0748MBFTS/ref=sr_1_5?s=electronics&ie=UTF8&qid=1515127853&sr=1-5&keywords=raspberry+pi+zero)
* [Hologram Nova USB Modem](https://hologram.io/nova/)
* [PNY PowerPack](https://www.amazon.com/gp/product/B00L9BU8Y2/ref=oh_aui_detailpage_o09_s00?ie=UTF8&psc=1)
* [Infrared Night Vision Camera](https://www.amazon.com/gp/product/B0759GYR51/ref=oh_aui_detailpage_o00_s00?ie=UTF8&psc=1)
* [Pulse Sensor](https://www.adafruit.com/product/1093)
* [MCP3008 Analog-Digital converter](https://www.adafruit.com/product/856)
* [Temperature Sensor](https://www.adafruit.com/product/374)
* [Accelerometer](https://www.adafruit.com/product/1231)
* Dog vest of choice


## Software
Requirements:
- [Raspbian Jessie image 2017-06-21](http://downloads.raspberrypi.org/raspbian/images/raspbian-2017-06-23/2017-06-21-raspbian-jessie.zip)
- [OpenCV for Pi Zero](https://www.pyimagesearch.com/2015/12/14/installing-opencv-on-your-raspberry-pi-zero/) or [OpenCV for Pi 3](https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/)
- Apache2 server
- [Tensorflow for Pi Zero](https://petewarden.com/2017/08/20/cross-compiling-tensorflow-for-the-raspberry-pi/) or [Tensorflow for Pi 3](https://github.com/samjabrahams/tensorflow-on-raspberry-pi)
- Numpy
- [Keras2](https://nikhilraghava.wordpress.com/2017/08/05/installing-keras-on-raspberry-pi-3/)
- [hologram-python-sdk](https://github.com/hologram-io/hologram-python)
- [YOLO on Raspian](https://github.com/PiSimo/PiCamNN)
- [Adafruit Python ADXL345](https://github.com/adafruit/Adafruit_Python_ADXL345)

## Wiring the Sensors
Here is a diagram showcasing how the temperature, pulse, and accelerometer sensors should be wired. We wired all these
sensors to a small pcb board for more reliable connections while the vest is worn. You should connect the Hologram Nova
via a usb port (for the zero we used a microusb to usb converter). You should also connect the pi camera using the mini
camera ribbon. 
![Wiring](http://mayorquinmachines.ai/images/poochpak_bb.png)

## Install
Compatibility between project dependencies requires python3.4 as default python3. You should burn
[this](http://downloads.raspberrypi.org/raspbian/images/raspbian-2017-06-23/2017-06-21-raspbian-jessie.zip) specific
image for your raspberry pi zero. 
After making this image and wiring the pi, boot up and go through the first-time boot configuration.
You should make sure to: 
* Under *Advanced Options*, Expand filesystem
* Under *Localization Options* change timezone 
* Change User password
* Under *Interfacing Options*, enable ssh, camera, SPI, IC2, and Serial

After a reboot, git clone this repo
```
cd ~/
git clone https://github.com/mayorquinmachines/PoochPak.git
cd PoochPak
```
Run the install script to install all dependencies. Note: This will take a **long** time! Leave it running overnight.
```
./install.sh
```
Reboot your pi after the install script has finished. Run:
```
sudo modprobe bcm2835-v4l2
sudo modprobe w1-gpio
sudo modprobe w1-therm
```
This is just making sure all modules needed to communicate with the sensors are enabled.


#### Setting up Hologram
To use hologram to send SMS, you'll need to set up you Hologram Dashboard and activate your sim card.
[Here](https://www.hackster.io/hologram/hologram-python-sdk-sending-data-45f305) is the Hologram starter guide for doing
just that. The install script has handled installing hologram-cli and hologram-python-sdk for you. You can test this
by running
```
sudo hologram version
```
Once your sim card is activated and your device shows that it is live in your Dashboard, you want to set up a phone
number you want to send SMS messages to. In your Dashboard, click on your device and navigate to *Configuration*. From
that page, you'll want to configure your phone number under **Configure phone number**. This should set up you Nova to
send SMS messages to this phone number. In this same page, you'll see **+ Show Device Key**. Clicking on this button
will give you a key you'll need to authenticate your hologram-python-sdk. You'll want to create a config file where 
you'll place this key for use. Run the following:
```
cd ~/PoochPak
touch config.py
echo "DEVICEKEY='<your-key-here>'" >> config.py
```

## Run
Finally, to run the code for object recognition and starting the sensor server, follow the instructions below!

#### Starting YOLO object recognition
``` 
cd yolo_picam/
nohup sudo python3 picam.py &
```

#### Starting Server
``` 
nohup sudo python poochpak_server.py &
```

## Troubleshooting
If you're having issues with the Yolo object recognitition script (picam.py) not finding the camera, it could be that
you need to reenable the camera again. Try enabling it again using ```sudo raspi-config``` and run ```sudo modprobe
bcm2835-v4l2```. 

Sometimes the Hologram Nova loses signal. You should make sure that the red LED is lit up and the blue LED is flashing.
Rapid flashing means you're on the 3G network, slower flashing means 2G network, and no blue light means the Nova isn't
on a network yet.

If the sensors aren't working correctly, take a look at the wiring again and make sure everything is correct. Then try
reenabling their modules again:
```
sudo modprobe w1-gpio  #For temp sensor
sudo modprobe w1-therm  #For temp sensor

sudo modprobe spi-bcm2708 #For pulse sensor
```
There are also a script you can run to test all of the sensors. Try running ``` python ~/PoochPak/tests/run_tests.py```

