## DoorPi

#### Overview:

The aim of this project is to create a low-cost, customizable security system using a Raspberry Pi.  This particular version
uses motion and door sensors to detect entry, but in theory other sensors could be used as well.  An NFC card or key fob
is used to arm/disarm the system.  Alarm status is indicated by sounds and addressable LED animations.  When an entry is 
detected, the Pi's camera records video and send email notifications.

#### Required Parts:
* Raspberry Pi (I used a model B) with SD card, case and power supply
* RPi Camera
* PIR sensor (https://www.adafruit.com/products/189)
* Door sensor (https://www.adafruit.com/products/375)
* PN532 NFC/RFID board (https://www.adafruit.com/product/364)
* LED ring (https://www.adafruit.com/products/1586)
* 5v 1A power supply for LED ring
* teensy 3.0 (https://www.pjrc.com/store/teensy3.html)
* micro USB cable to connect RPi to teensy
* small speaker to play sounds from RPi
* USB hub (optional)
* jumper wires and headers

#### Required Software:
* mpg321 for playing sounds
* libnfc with nfc-eventd for running scripts when NFC cards are scanned
* RPi.GPIO python library

#### Summary of Operation:

1. Scan NFC.
2. Sec/arm-disarm.sh toggles /var/lib/misc/alarm between ARMED and DISARMED, run countdown and run python sensor script to continuously check sensors.
3. If sensors are triggered, take video, play sounds/LED animations, and countdown before sending email notification.
4. Scan NFC to kill the sensor script and return alarm status to DISARMED.

[Here](https://youtu.be/7nwuVskN5R8) is a video of the system in action.

#### Description of Included Files:

The arm-disarm.sh script is triggered by the nfc-eventd daemon whenever an NFC card is scanned.  This script verifies
the NFC card, plays sounds, sends LED animation commands to the teensy microcontroller and starts/stops the sensor 
script.

The sensor.py script is the core of the alarm system.  It checks the sensors every half second, and if they're triggered,
it plays LED animations and warning sounds, starts/stops the camera recording, and sends email notifications.  

The reset-alarm.sh script will restart the sensor script if the pi was shut down while the alarm was armed.  It is run
at startup by appending it to the rc.local file.

The nfc-eventd.conf file is the configuration file for nfc-eventd.  It contains information about the NFC driver and 
controls which scripts are run and when.  

The ring-send.py script sends commands over UART to the teensy that controls the LED ring.

The ring.ino file contains all the LED animations.  This is compiled and loaded onto the teensy using teensyduino.

The sensor-test.py script helps calibrate your sensors.

The picrontab will move all recorded video to a remote server once a day.

#### Additional Resources:

This tutorial provides a good explanation on how to connect and read sensors with a Raspberry Pi.
https://learn.adafruit.com/adafruits-raspberry-pi-lesson-12-sensing-movement

Licensed under GNU GPLv3