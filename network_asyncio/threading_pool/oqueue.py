import threading

class ThreadSafeQueue(object):
    def __init__(self, max_size=0, *args, **kw):
        # 用列表假装队列
        self.queue = list()
        self.index = 0
        self.max_size = max_size
        self.lock = threading.RLock()
        self.condition = threading.Condition()

    @property
    def size(self):
        self.lock.acquire()
        size = len(self.queue)
        self.lock.release()
        return size

    def wait(self, value, timeout=10):
        print('waiting ', value)
        self.condition.acquire()
        self.condition.wait(timeout=timeout)
        self.condition.release()

    def notify(self):
        self.condition.acquire()
        self.condition.notify()
        self.condition.release()

    def pop(self):
        if not self.size:
            self.wait('product', timeout=3)
        self.lock.acquire()
        item = None
        if self.size:
            item = self.queue.pop()
        self.lock.release()
        self.notify()
        return item

    def put(self, item):
        if self.max_size != 0 and self.size  >= self.max_size:
            self.wait('consume')
        self.lock.acquire()
        self.queue.append(item)
        self.lock.release()
        self.notify()

    def batch_put(self, items):
        if isinstance(items, list):
            items = list(items)
        for item in items:
            self.put(item)

    def sort(self, func):
        print('sort　start........')
        self.lock.acquire()
        self.queue = func(self.queue)
        self.pp()
        self.lock.release()
        print('sort　end........')

    def pp(self):
        self.lock.acquire()
        print('当前队列:', '\t'.join([str(each) for each in self.queue]))
        self.lock.release()

    def get(self, index):
        self.lock.acquire()
        item = self.queue[index]
        self.lock.release()
        return item

    # 无法保持线程安全,故不适用
    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.queue):
            item = self.queue[self.index]
            self.index += 1
            return item
        self.lock.acquire()
        self.index = 0
        self.lock.release()
        raise StopIteration("到头了...")
