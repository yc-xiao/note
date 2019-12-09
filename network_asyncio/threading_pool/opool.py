'''
    1.线程池用于并发执行任务。
        新增，获取，查看任务。　
        启动，停止，继续，线程。
        因为线程是并发的，所以需要一个安全队列
'''
from .oqueue import ThreadSafeQueue
from .othread import Thread
from .otask import Task

from functools import wraps
import threading
import psutil

class ThreadPool(object):
    def __init__(self, size=0, *args, **kw):
        if not size:
            size = psutil.cpu_count() * 2
        self.size = size
        self.pool = ThreadSafeQueue(size)
        self.task_queue = ThreadSafeQueue()
        # 查看任务数量，当任务数量超过1万,iter_flag设为false,反之为true
        self.iter_flag = False

        for i in range(size):
            thread = Thread(task_queue=self.task_queue)
            # thread.start()
            self.pool.put(thread)

    def pp(msg):
        def wrap(func):
            @wraps(func)
            def inner(*args, **kw):
                # 监控每个函数执行
                print(f'start: {msg}')
                result = func(*args, **kw)
                print(f'end: {msg}')
                return result
            return inner
        return wrap

    @pp('启动线程池')
    def start(self):
        for index in range(self.pool.size):
            thread = self.pool.get(index)
            thread.start()

    def is_ko(self):
        while self.task_queue.size:
            pass
        print('任务全部执行完')

    def put_task(self, task):
        self.task_queue.put(task)

    @pp('批量添加任务，控制线程')
    def batch_put_task_and_console_thread(self, tasks):
        self.wait()
        self.batch_put_task(tasks)
        self.go()

    @pp('批量添加任务')
    def batch_put_task(self, tasks):
        if isinstance(tasks, list):
            tasks = list(tasks)
        for task in tasks:
            self.put_task(task)

    def get_task(self, index):
        return self.task_queue.get(index)

    def get_task_queue(self):
        return self.task_queue

    @pp('唤醒线程')
    def go(self):
        if self.iter_flag:
            for thread in self.pool:
                thread.go()
        else:
            for index in range(self.pool.size):
                thread = self.pool.get(index)
                thread.go()

    @pp('线程等待')
    def wait(self):
        if self.iter_flag:
            for thread in self.pool:
                thread.wait()
        else:
            for index in range(self.pool.size):
                thread = self.pool.get(index)
                thread.wait()

    @pp('kill线程')
    def stop(self):
        if self.iter_flag:
            for thread in self.pool:
                thread.stop()
        else:
            for index in range(self.pool.size):
                thread = self.pool.get(index)
                thread.stop()

    def delete_task(self, task):
        pass

    def bacth_delete_task(self, tasks):
        pass


"""
def cal_num():
    count = 1
    for i in range(100000):
        count += i
    return count
def test_tread_pool():
    pool = ThreadPool()
    tasks = [Task(func=cal_num, desc='test') for i in range(100)]
    pool.batch_put_task(tasks) # 批量添加任务
    pool.start()    # 启动线程池
    pool.is_ko()    # 等待任务完成
    pool.batch_put_task_and_console_thread(tasks) # 重新添加任务
    pool.is_ko()    # 等待任务完成
    pool.stop()     # 关闭线程池 close()
"""
