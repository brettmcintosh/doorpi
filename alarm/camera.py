from picamera.camera import PiCamera
from datetime import datetime

import alarm.settings as settings


class Camera(PiCamera):
    """Pi camera configured for DoorPi."""

    @staticmethod
    def get_video_path():
        # returns the absolute path for new video files based on a timestamp
        return settings.VIDEO_PATH + "%s.h264" % datetime.now().strftime("%Y%m%d_%H-%M-%S")

    def configure(self):
        self.rotation = settings.CAMERA_ROTATION
        self.resolution = settings.CAMERA_RESOLUTION
        self.framerate = settings.CAMERA_FRAMERATE