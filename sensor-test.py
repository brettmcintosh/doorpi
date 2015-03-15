# This script is useful for calibrating your sensors.  It simply prints the sensor name
# and a timestamp whenever the sensor is triggered.  

from time import sleep
from datetime import datetime
import RPi.GPIO as io

io.setmode(io.BCM)
pir_pin = 18
door_pin = 23

io.setup(pir_pin, io.IN)         # activate input
io.setup(door_pin, io.IN, pull_up_down=io.PUD_UP)  # activate input with PullUp

while True:

    # timestamp
    now = datetime.now()

    # check for motion
   if io.input(pir_pin):
       print "PIR %s" % now

    # check door
    if io.input(door_pin):
	print "DOOR %s" % now

    sleep(.5)
