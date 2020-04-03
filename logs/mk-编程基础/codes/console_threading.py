import threading
import time


class Cthread(threading.Thread):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.run_flag = threading.Event()
        self.stop_flag = threading.Event()
        self.run_flag.set()
        self.stop_flag.clear()

    def run(self):
        while self.run_flag.is_set():
            self.stop_flag.wait() # 如果stop_flag为0则等待，可设置等待时间
            print('running.......')
            time.sleep(1)

    def pause(self):
        self.stop_flag.clear()

    def resume(self):
        self.stop_flag.set()

    def stop(self):
        self.stop_flag.set()
        self.run_flag.clear()

if __name__ == '__main__':
    th = Cthread()
    th.start()
    time.sleep(3)
    th.resume()
    time.sleep(3)
    th.pause()
    time.sleep(3)
    th.resume()
    time.sleep(3)
    th.stop()
