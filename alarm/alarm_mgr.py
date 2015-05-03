from passlib.hash import sha256_crypt
import threading
import SocketServer
import socket
import json
import time

import settings
from camera import Camera
from sensor import Sensor
from notification import LEDRing


ALARM_CODES = (settings.ARMED, settings.DISARMED)
ARMED = settings.ARMED
DISARMED = settings.DISARMED


class AlarmManager(object):

    def __init__(self):
        self.camera = None
        self.sensors = {}
        self.sensor_scan_thread = None
        self._stop_sensor_scan = False
        self._sensor_scan_stopped = threading.Event()
        self._lock = threading.Lock()
        self._status = None
        self.is_triggered = False
        self.sent_notification = False
        self.server = None

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        assert status in ALARM_CODES
        # save status to STATUS_PATH file
        with open(settings.STATUS_FILE_PATH, 'w') as f:
            f.write(status)

    def update_status_from_file(self):
        with open(settings.STATUS_FILE_PATH, 'r') as f:
            status = f.read().strip()
        if status not in ALARM_CODES:
            raise SettingsError('Invalid status in STATUS_FILE_PATH file or ARMED/DISARMED settings misconfigured.')
        self._status = status

    def setup(self):

        # add camera
        if settings.CAMERA:
            camera = Camera()
            camera.configure()
            self.camera = camera

        # add sensors
        self.setup_sensors()

        # read status from file
        self.update_status_from_file()

        # create and start server
        self.server = AlarmSocketServer.start()

    def setup_sensors(self):
        # add sensors
        for sensor in settings.SENSORS:
            s = Sensor(**sensor)
            s.setup()
            self.sensors[s.name] = s

    def scan_sensors(self, refresh_rate=.25):
        self._sensor_scan_stopped.clear()
        # scan all sensors continuously

        while not self._stop_sensor_scan:
            for sensor in self.sensors.values():
                if sensor.read():
                    # do something; don't forget to Lock!
                    request_dict = {'action': 'sensor', 'sensor': sensor.name}
                    self.handle_request(request_dict)
                    # with self._lock:
                    #     if not self.is_triggered:
                    #         self.is_triggered = True
                    # print('%s activated' % sensor.name)

            time.sleep(refresh_rate)
        self._sensor_scan_stopped.set()

    def start_sensor_scan(self):
        sensor_scan_thread = threading.Thread(target=self.scan_sensors)
        self.sensor_scan_thread = sensor_scan_thread
        sensor_scan_thread.daemon = True
        sensor_scan_thread.start()

    def stop_sensor_scan(self):
        self._stop_sensor_scan = True
        self._sensor_scan_stopped.wait()
        self._stop_sensor_scan = False

    def arm(self):
        pass

    def disarm(self):
        pass

    def handle_request(self, request_dict):
        action = request_dict['action']

        if action == 'nfc':
            self.handle_nfc_request(request_dict)

        elif action == 'sensor':
            self.handle_sensor_request(request_dict)

    def handle_nfc_request(self, request_dict):
        print('NFC Scan')

    def handle_sensor_request(self, request_dict):
        print('Sensor Event')

    @staticmethod
    def key_valid(unverified_key):

        for verified_hash in settings.KEY_HASHES:
            if sha256_crypt.verify(unverified_key, verified_hash):
                return True

        return False


class AlarmRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024)
        # parse json
        try:
            request = json.loads(data)
        except ValueError:
            request = {"action": "None"}
            print("Not JSON...")
        # pass request dictionary to the manager's request handler
        self.request.sendall('received : %s' % data)
        self.server.mgr.handle_request(request)

        # print(data)
        # response = "You said: %s. Triggered: %s. Thread: %s.\n" % (data,
        #                                                            self.server.mgr.is_triggered,
        #                                                            threading.current_thread().name)
        # if not self.server.mgr.is_triggered:
        #     self.server.mgr.is_triggered = True
        # else:
        #     self.server.mgr.is_triggered = False
        # self.request.sendall(response)


class AlarmSocketServer(SocketServer.ThreadingTCPServer):

    def __init__(self, server_address, handler, mgr=None):
        SocketServer.ThreadingTCPServer.__init__(self, server_address, handler, bind_and_activate=True)
        self.mgr = mgr

    @classmethod
    def start(cls):
        new_server = cls(('0.0.0.0', 5555), AlarmRequestHandler)
        listen_thread = threading.Thread(target=new_server.serve_forever)
        listen_thread.daemon = True
        listen_thread.start()
        return new_server


class SettingsError(Exception):
    pass


def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        response = sock.recv(1024)
        print "Received: {}".format(response)
    finally:
        sock.close()


if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "0.0.0.0", 8080


    mgr = AlarmManager()

    server = AlarmSocketServer((HOST, PORT), AlarmRequestHandler, mgr=mgr)
    ip, port = 'localhost', 8080


    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print "Server loop running in thread:", server_thread.name

    # message1 = json.dumps({'action': 'nfc_scan', 'show': 'Simpsons'})
    # message2 = json.dumps({'action': 'sensor', 'show': 'Simpsons'})
    #
    # for _ in xrange(50):
    #     start = time.time()
    #     client(ip, port, message1)
    #     client(ip, port, message2)
    #     end = time.time()
    #     print(str(end-start))
    #
    # server.shutdown()
    # del server

