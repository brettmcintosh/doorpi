#!/usr/bin/env python

import serial
import sys


def ring(command):
    s = serial.Serial(sys.argv[1], 9600)
    s.write(command)
    s.close()

ring(sys.argv[2])
