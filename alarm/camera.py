from picamera.camera import PiCamera
from datetime import datetime

from alarm import settings


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

    def start_recording(self, output, format=None, resize=None, splitter_port=1, **options):
        output = self.get_video_path()
        super(Camera, self).start_recording(self, output, format, resize, splitter_port, **options)
