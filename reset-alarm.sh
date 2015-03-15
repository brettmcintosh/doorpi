#!/bin/bash

# if the pi is rebooted while still armed, this script will restart the sensor script.

# check the alarm file for ARMED status
if [ "$(cat /var/lib/misc/alarm)" == "ARMED" ]
then
	# restart the sensor script
    /home/pi/sec/sensor.py &
fi
