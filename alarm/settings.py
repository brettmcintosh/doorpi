CAMERA = True
CAMERA_ROTATION = 180
CAMERA_RESOLUTION = (1400, 1400)
CAMERA_FRAMERATE = 15

VIDEO_PATH = "/home/pi/camera/"
STATUS_FILE_PATH = "/var/lib/misc/alarm"
LOG_FILE_PATH = "/home/pi/sec/sensor.log"

# To add a key, use import alarm.alarm_mgr; alarm.alarm_mgr.AlarmManager.add_new_key()
KEY_HASHES = ('',
              '12345',
              '67890', )

MOTION_SENSOR = {'pin': 18,
                 'name': 'Motion Hallway'}

DOOR_SENSOR = {'pin': 23,
               'pull_up': True,
               'name': 'Door'}

SENSORS = [MOTION_SENSOR, DOOR_SENSOR]

ARMED = 'ARMED'
DISARMED = 'DISARMED'

LED_DEVICE_PATH = '/dev/ttyACM0'
LED_DEVICE_BAUDRATE = 9600