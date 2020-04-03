import uuid

class Task(object):
    def __init__(self, func, *args, **kw):
        self.id = uuid.uuid4()
        self.callable = func
        self.args = args
        self.kw = kw
    def __str__(self):
        return 'Task id:' + str(self.id)

class AsyncTask(Task):
    def __init__(self, func, *args, **kw):
        self.result = None
        self.condition = threading.Condition()
        super().__init__(func, *args, **kw)

    def set_result(self, result):
        self.condition.acquire()
        self.result = result
        self.condition.notify()
        self.condition.release()

    def get_result(self):
        self.condition.acquire()
        if not self.result:
            self.condition.wait()
        result = self.result
        self.condition.release()
        return result


if __name__ == '__main__':
    task = Task(func=None)
    print(task)
