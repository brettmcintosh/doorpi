import settings as settings
from camera import Camera

class AlarmManager(object):

    def __init__(self):
         self.camera = None
         self.sensors = []
         self.status = None
         self.is_triggered = False
         self.sent_notification = False

    def setup(self):

        if settings.CAMERA:
