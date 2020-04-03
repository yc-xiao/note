from quere import ThreadSafeQueue
from task import Task, AsyncTask
import threading
import time

class ProcessThread(threading.Thread):
    def __init__(self, task_queue, *args, **kw):
        threading.Thread.__init__(self, *args, **kw)
        # 线程停止标志
        self.dismiss_flag = threading.Event()
        # 任务队列(处理线程从队列中取出的任务)
        self.task_queue = task_queue
        self.args = args
        self.kw = kw

    def run(self):
        while True:
            # 判断线程是否被要求停止
            if self.dismiss_flag.is_set():
                break
            task = self.task_queue.pop()
            if not isinstance(task, Task):
                continue
            # 执行任务
            result = task.callable(*task.args, **task.kw)
            if isinstance(task, AsyncTask):
                task.set_result(result)
            time.sleep(0.2)

    def dismiss(self):
        self.dismiss_flag.set()

    def stop(self):
        self.dismiss()

class Pool(object):
    def __init__(self, size=0):
        if not size:
            size = 4 * 2 # 最优为CPU核数的两倍
        self.pool = ThreadSafeQueue(size)
        self.task_queue = ThreadSafeQueue()

        for i in range(size):
            self.pool.put(ProcessThread(self.task_queue))

    def start(self):
        for i in range(self.pool.size()):
            thread = self.pool.get(i)
            thread.start()

    # 停止线程
    def join(self):
        for i in range(self.pool.size()):
            thread = self.pool.get(i)
            thread.stop()
        while self.pool.size():
            thread = self.pool.pop()
            thread.join()

    # 向线程池提交任务
    def put(self, item):
        if not isinstance(item, Task):
            raise Exception('你的任务有点问题!')
        self.task_queue.put(item)

    def batch_put(self, items):
        if not isinstance(items, list):
            items = list(items)
        for item in items:
            self.put(item)

    def size(self):
        return self.pool.size()
