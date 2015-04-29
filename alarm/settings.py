CAMERA = True
CAMERA_ROTATION = 180
CAMERA_RESOLUTION = (1400, 1400)
CAMERA_FRAMERATE = 15

VIDEO_PATH = "/home/pi/camera/"
STATUS_FILE_PATH = "/var/lib/misc/alarm"
LOG_FILE_PATH = "/home/pi/sec/sensor.log"

# use passlib.hash.sha256_crypt.encrypt("password")
KEY_HASHES = ('', )

MOTION_SENSOR = {'pin': 18,
                 'name': 'Motion Hallway'}

DOOR_SENSOR = {'pin': 23,
               'pull_up': True,
               'name': 'Door'}

SENSORS = [MOTION_SENSOR, DOOR_SENSOR]

ARMED = 'ARMED'
DISARMED = 'DISARMED'

LED_DEVICE_PATH = ''
LED_DEVICE_BAUDRATE = 9600