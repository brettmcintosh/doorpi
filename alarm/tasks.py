from celery import Celery
import pygame.mixer as mix    # pygame should already be installed on raspbian

from notification import LEDRing


app = Celery('tasks', backend='amqp', broker='amqp://')


@app.task
def send_LED_command(command):

    with LEDRing() as ring:
        ring.send_command(command)


@app.task
def play_sound(sound_file):

    mix.init()
    mix.music.load(sound_file)
    mix.music.play()
    while mix.music.get_busy():
        continue


@app.task
def start_recording():

    pass