import threading
import uuid

class Task(object):
    def __init__(self, func, desc=None, args=(), **kw):
        self.id = uuid.uuid4()
        self.func = func
        self.desc = desc
        self.args = args
        self.kw = kw
        self.result = None
        self.flag = False
        self.priority = 0

    def __repr__(self):
        attrs = ('id', 'desc', 'priority', 'flag', 'result')
        return '\n'.join([f'task {key}: {getattr(self, key)}' for key in attrs])

    def run(self):
        result = self.func(*self.args, **self.kw)
        self.flag = True
        self.result = result
