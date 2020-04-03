from collections import deque
import threading

class ThreadSafeQueue(object):
    def __init__(self, max_size=0):
        self.queue = []
        self.max_size = max_size
        self.lock = threading.Lock()
        self.condition = threading.Condition()

    def size(self):
        self.lock.acquire()
        size = len(self.queue)
        self.lock.release()
        return size

    def put(self, item):
        if self.size !=0 and self.size() > self.max_size:
            raise Exception('满了!')
        self.lock.acquire()
        self.queue.append(item)
        self.lock.release()
        # 通知其他线程可以继续进行,通知之前需要先锁，避免重复通知

        self.condition.acquire()
        self.condition.notify()
        self.condition.release()

    def batch_put(self, items):
        if not isinstance(items, list):
            items = [items]
        for item in items:
            self.put(item)

    def pop(self, block=False, timeout=0):
        if not self.size():
            if block:
                self.condition.acquire()
                self.condition.wait(timeout=timeout)
                self.condition.release()
            else:
                return None
        self.lock.acquire()
        item = None
        if self.size() > 0:
            item = self.queue.pop()
        self.lock.release()
        return item

    def get(self, index):
        self.lock.acquire()
        item = self.queue[index]
        self.lock.release()
        return item

import time
queue = ThreadSafeQueue(max_size=20)

def producer():
    while True:
        time.sleep(1) # 让出当前进程内的cpu给其他线程
        queue.put(1)

def consumer():
    while True:
        time.sleep(0.1) # 让出当前进程内的cpu给其他线程
        item = queue.pop(timeout=0.5)
        print(item)

if __name__ == '__main__':
    th1 = threading.Thread(target=producer)
    th2 = threading.Thread(target=consumer)
    th1.start()
    th2.start()
    th1.join()
    th2.join()
