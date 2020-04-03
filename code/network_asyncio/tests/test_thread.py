import threading
import time

class ThreadEvent(threading.Thread):
    def __init__(self, *args, **kw):
        self.flag = threading.Event()
        self.wflag = threading.Event()
        self.flag.set()
        super().__init__(*args, **kw)

    def run(self):
        print('线程启动!')
        while self.flag.is_set():
            print('线程执行中，占用cpu!!!')
            if self.wflag.wait():
                print('线程执行内部逻辑')
            time.sleep(0.5)

    def wait(self):
        print('退出内部逻辑!')
        time.sleep(1)
        self.wflag.clear()

    def go(self):
        print('进入内部逻辑!')
        time.sleep(1)
        self.wflag.set()

    def stop(self):
        # 如果事件event等待了需要处理，不然会一直等待
        self.wflag.set()
        self.flag.clear()
        print('线程结束')

def test_thread_event():
    thread = ThreadEvent()
    actions = ('start', 'go', 'wait', 'go', 'wait', 'stop', 'join')
    for action in actions:
        getattr(thread, action)()

def main():
    test_thread_event()


if __name__ == '__main__':
    main()
