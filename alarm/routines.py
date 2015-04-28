from alarm import settings
from datetime import datetime


class BaseRoutine(object):

    def __init__(self):
        self.start_time = datetime.now()
        self.start_message = ''
        self.end_message = ''
        self.tasks = ()

    def seconds_since_start(self):
        time_since = datetime.now() - self.start_time
        return time_since.seconds

    def log(self):
        pass

    def start(self):
        pass

    def cancel(self):
        pass


class EntryRoutine(BaseRoutine):

    def __init__(self):
        super(EntryRoutine, self).__init__()
        self.tasks = ()


class ArmRoutine(BaseRoutine):

    def __init__(self):
        super(ArmRoutine, self).__init__()
        self.tasks = ()


class DisarmRoutine(BaseRoutine):

    def __init__(self):
        super(DisarmRoutine, self).__init__()
        self.tasks = ()