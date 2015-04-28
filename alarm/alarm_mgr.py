from passlib.hash import sha256_crypt

from alarm import settings
from camera import Camera
from sensor import Sensor
from notification import LEDRing


ALARM_CODES = (settings.ARMED, settings.DISARMED)
ARMED = settings.ARMED
DISARMED = settings.DISARMED


class AlarmManager(object):

    def __init__(self):
        self.camera = None
        self.sensors = set()
        self._status = None
        self.is_triggered = False
        self.sent_notification = False

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        assert status in ALARM_CODES
        # save status to STATUS_PATH file
        with open(settings.STATUS_FILE_PATH) as f:
            f.write(status)

    def update_status_from_file(self):
        with open(settings.STATUS_FILE_PATH) as f:
            status = f.read()
        self._status = status

    def setup(self):

        # add camera
        if settings.CAMERA:
            camera = Camera()
            camera.configure()
            self.camera = camera

        # add sensors
        for sensor in settings.SENSORS:
            s = Sensor(**sensor)
            s.setup()
            self.sensors.add(s)

        # read status from file
        self.update_status_from_file()
        if self.status not in ALARM_CODES:
            raise SettingsError('Invalid status in STATUS_FILE_PATH file or ARMED/DISARMED settings misconfigured.')

    def arm(self):
        pass

    def disarm(self):
        pass

    @staticmethod
    def key_valid(unverified_key):

        for verified_hash in settings.KEY_HASHES:
            if sha256_crypt.verify(unverified_key, verified_hash):
                return True

        return False


class SettingsError(Exception):
    pass