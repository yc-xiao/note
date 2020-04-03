from .otask import Task
import threading
import time

'''
    Event 一个线程标志位，可以生成多个标志位用于控制线程。
    创建线程类
        1.永不被回收，故run一直while
        2.可以暂停，启动
'''

class Thread(threading.Thread):
    def __init__(self, task_queue, *args, **kw):
        self.task_queue = task_queue
        self.flag = threading.Event()
        self.dismiss_flag = threading.Event()
        self.flag.set()
        self.dismiss_flag.set()
        super().__init__(*args, **kw)

    def run(self):
        while self.dismiss_flag.is_set():
            if self.flag.is_set():
                task = self.task_queue.pop() # 这个会造成死锁
                if isinstance(task, Task):
                    task.run()

    # 停止线程任务
    def wait(self):
        self.flag.clear()

    # 执行线程任务
    def go(self):
        self.flag.set()

    # 退出线程，退出后这个线程就么有用了
    def stop(self):
        self.dismiss_flag.clear()
        print('退出线程')
