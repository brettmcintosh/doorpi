import RPi.GPIO as io


class Sensor(object):

    def __init__(self, pin=None, mode=io.BCM, name='', pull_up=False):
        self.pin = pin
        self.mode = mode
        self.name = name
        self.pull_up = pull_up

    def setup(self):
        io.setmode(self.mode)

        if self.pull_up:
            io.setup(self.pin, io.IN, pull_up_down=io.PUD_UP)
        else:
            io.setup(self.pin, io.IN)

    def read(self):
        if io.input(self.pin):
            return True
        return False


class SensorManager(object):

    def cleanup(self):
        io.cleanup()