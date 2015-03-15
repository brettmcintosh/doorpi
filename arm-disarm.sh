#!/bin/bash

# put all approved NFC IDs in this array.  these are basically the keys that can arm/disarm the alarm.  
# I used MiFare NFC cards but Muni cards work as well.
keys = ("12345678" "87654321") 

verified=false

# see if key is in key array
for key in "${keys[@]}"
do
    if [ "$1" == "$key" ]
    then
        export verified=true
        echo "PERMISSION GRANTED\n"

        # log the event
        echo "$(date '+%Y-%m-%d %H:%M:%S') NFC Tag Verified" >> /home/pi/sec/sensor.log
        break
    fi
done

# log event and exit if key is not approved
if [ "$verified" == "false" ]
then
    echo -e "PERMISSION DENIED\n"

    # log the event then exit
    echo "$(date '+%Y-%m-%d %H:%M:%S') NFC Tag Not Valid" >> /home/pi/sec/sensor.log
    exit 0
fi

# if the alarm file says the alarm is disarmed and the NFC card is valid,
# play the arming system sound, trigger the LED countdown animation and wait 18 seconds.
if [ "$(cat /var/lib/misc/alarm)" == "DISARMED" ] && [ "$verified" == "true" ]
then
    echo "System will be armed in 18 seconds..."

    # play the arming system sound
    mpg321 /home/pi/sec/doorsounds/armingsystem.mp3 &

    # the LED ring is controlled by a teensy microcontroller connected over UART
    # the "c" command triggers the countdown animation.
    /home/pi/ring/ring-send.py $(echo "/dev/$(ls /dev | grep [t]tyACM)") "c"
    sleep 18

    # the "m" command triggers the armed animation
    /home/pi/ring/ring-send.py $(echo "/dev/$(ls /dev | grep [t]tyACM)") "m"

    # change the status to ARMED in the alarm file
    echo ARMED > /var/lib/misc/alarm

    # record the event in the log
    echo "$(date '+%Y-%m-%d %H:%M:%S') System Armed" >> /home/pi/sec/sensor.log

    # play the system armed warning sound
    mpg321 /home/pi/sec/doorsounds/systemarmed.mp3 &

    # start the sensor script to check for motion and record video
    /home/pi/sec/sensor.py &

# if alarm file says the alarm is armed and the NFC card is valid,
# stop the sensor script, play the system disarmed sound and trigger the disarmed animation
elif [ "$(cat /var/lib/misc/alarm)" == "ARMED" ] && [ "$verified" == "true" ]
then
    # stop sensor script then disarm
    kill $(ps aux | grep '[p]ython /home/pi/sec/sensor.py' | awk '{print $2}')

    # change the alarm file status to DISARMED
    echo DISARMED > /var/lib/misc/alarm

    #play the system disarmed sound
    mpg321 /home/pi/sec/doorsounds/systemdisarmed.mp3 &

    # the "T" command stops any active LED animations
    /home/pi/ring/ring-send.py $(echo "/dev/$(ls /dev | grep [t]tyACM)") "T"

    # wait half a second for the command to register
    sleep .5

    # the "r" command triggers the disarmed animation
    /home/pi/ring/ring-send.py $(echo "/dev/$(ls /dev | grep [t]tyACM)") "r"

    # record the event in the log
    echo "$(date '+%Y-%m-%d %H:%M:%S') System Disarmed" >> /home/pi/sec/sensor.log

fi
