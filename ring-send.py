#!/usr/bin/env python

# this script sends commands to the teensy microcontroller that controls the LED ring.
# the first argument is the serial device (usually /dev/ttyACM0) and the second argument
# is the LED animation command.

import serial
import sys


def ring(command):

	# start serial connection and send command
    s = serial.Serial(sys.argv[1], 9600)
    s.write(command)
    s.close()

ring(sys.argv[2])
