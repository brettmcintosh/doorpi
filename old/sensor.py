#!/usr/bin/env python

from datetime import datetime, timedelta
from time import sleep
import picamera
import os
import subprocess
import smtplib
import RPi.GPIO as io
import serial

# set up GPIO and assign pins
io.setmode(io.BCM)
pir_pin = 18
door_pin = 23

# input for PIR motion sensor
io.setup(pir_pin, io.IN)

# input for door sensor
io.setup(door_pin, io.IN, pull_up_down=io.PUD_UP)

# set the path for the log file
file_path = "/home/pi/sec/sensor.log"

# configure the pi's camera
camera = picamera.PiCamera()
camera.rotation = 180
camera.resolution = (1400,1400)
camera.framerate = 15

# initialize variables
trigger = False
countdown = False
status = 'OK'
email_sent = False
message1 = ""
message2 = ""

def get_video_path():
    # returns the absolute path for new video files based on a timestamp
    return "/home/pi/camera/" + "%s.h264" % datetime.now().strftime("%Y%m%d_%H-%M-%S")

def smtp_send(timestamp, motion_status, door_status):
    # sends email notifications.  I set up a gmail account specifically for sending these notifications.

    # send notifications to your email and to your phone as text messages.  most carriers have an email to
    # text portal available for free.
    to = ['email_recipient@gmail.com', '1234567890@your_wireless_provider.net']
    gmail_user = 'your_pi_gmail_account@gmail.com'
    gmail_pwd = 'your_pi_gmail_password'

    # set up smtp connection over TLS.
    # USE TLS!  Don't be lazy!
    smtpserver = smtplib.SMTP("smtp.gmail.com", 587, 5)
    smtpserver.ehlo_or_helo_if_needed()
    smtpserver.starttls()

    # log in to gmail server
    smtpserver.login(gmail_user, gmail_pwd)

    # generate email header and message then send it
    header = 'To:' + to[0] + ',' + to[1] + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:Unauthorized Entry \n'
    msg = header + '\nThere was an unauthorized entry at %s.\n%s\n%s\n-doorpi' %(timestamp, message1, message2)
    smtpserver.sendmail(gmail_user, to, msg)
    smtpserver.close()


def send_email(motion_status, door_status):
    # This function is what actually calls the smtp_send function.  The nested try/except statements are necessary
    # due to gmail's greylisting policy, which rejects/defers connection attempts.  This is extrememly hacky and will 
    # eventually be improved, but for now it seems to work every time. :/
    try:
        smtp_send(datetime.now(), motion_status, door_status)
    except:
        try:
            smtp_send(datetime.now(), motion_status, door_status)
        except:
            with open(file_path, "a") as log:
                log.write("%s Email FAILED!\n" % datetime.now())

# This is the actual sensor loop.  The PIR motion and door sensors are read every half second.  If either sensor is
# triggered, the event is logged, the camera starts recording, an LED animation command is sent to the teensy, and the
# unauthorized access sound is played.  A countdown is also started and if the script isn't terminated within 20 seconds 
# (by scanning the NFC card and triggering the arm/disarm script), an email notification will be sent and the calling 
# police sound will be played (the police aren't actually called, it's just to scare the intruder).  The camera will 
# continue recording until there is no motion for 5 seconds.
if __name__ == "__main__":
    
    while True:

        # reset the sensor variables 
        motion = False
        door = False

        # check for motion
        if io.input(pir_pin):
            motion = True
            trigger = True
            message1 = "Motion Detected"
            with open(file_path, "a") as log:
                log.write("%s Motion Detected!\n" % datetime.now())

        # check door 
        if io.input(door_pin):
            door = True
            trigger = True
            message2 = "Door Opened"
            with open(file_path, "a") as log:
                log.write("%s Door Opened!\n" % datetime.now())
        
        # if either sensor is triggered
        if trigger and (motion or door):

            # play unauthorized access sound using mpg321
            subprocess.Popen("mpg321 /home/pi/sec/doorsounds/unauthorizedaccess.mp3", shell=True)

            # if the alarm has been triggered for the first time in the cycle, log the event, start the countdown,
            # and send the command for the countdown LED animation.
            if status == 'OK':
                status = 'ALARM'
                with open(file_path, "a") as log:
                    log.write("%s Alarm triggered!\n" % datetime.now())
                countdown = True
                initial_entry = datetime.now()
                subprocess.Popen('/home/pi/ring/ring-send.py $(echo "/dev/$(ls /dev | grep [t]tyACM)") "w"', shell=True)

            # if the alarm was previously triggered and the countdown is over, send the command for the alarm LED animation instead.
            else:
                countdown = False
                subprocess.Popen('/home/pi/ring/ring-send.py $(echo "/dev/$(ls /dev | grep [t]tyACM)") "m"', shell=True)

            # start recording the video is not already
            if not camera.recording:
                camera.start_recording(get_video_path())

                with open(file_path, "a") as log:
                    log.write("%s Starting camera...\n" % datetime.now())

                print("Starting video...")

            # countdown 20 seconds from the initial entry and then send an email notification
            if status != 'OK' and not email_sent:
                if (datetime.now() - initial_entry > timedelta(seconds=20)):
                    timestamp = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                    send_email(motion, door)
                    email_sent = True
                    with open(file_path, "a") as log:
                        log.write("%s Email sent!\n" % datetime.now())

                    # play the calling police sound (does not actually call police :p)
                    subprocess.Popen("mpg321 /home/pi/sec/doorsounds/callingpolice.mp3", shell=True)

                    # you can trigger additional actions here, e.g. posting a tweet or shutting down a server.

            # record for at least 5 seconds even if there is no motion
            camera.wait_recording(5)

        # stop camera when motion has stopped and door is closed
        elif trigger and not motion and not door:
            with open(file_path, "a") as log:
                log.write("%s Motion stopped and door closed. Stopping camera...\n" % datetime.now())
            print("Stopping video...")
            camera.stop_recording()

            # reset the trigger variable for the next iteration of the loop
        	trigger = False

            # delay for video processing
            sleep(1)

        # if neither sensor was triggered, wait a half second and check again
        else:
            sleep(.5)