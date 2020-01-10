"""
    询问操作交给OS
"""
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ
import socket

selector = DefaultSelector()
stopped = False
urls_todo = {'/', '/1', '/2', '/3', '/4', '/5', '/6', '/7', '/8', '/9'}


class Future:
    def __init__(self):
        self.result = None
        self._callbacks = []

    def add_done_callback(self, fn):
        self._callbacks.append(fn)

    def set_result(self, result):
        self.result = result
        for fn in self._callbacks:
            fn(self)


class Crawler:
    def __init__(self, url):
        self.url = url
        self.response = b''

    def fetch(self):
        sock = socket.socket()
        # 设置非阻塞
        sock.setblocking(False)
        try:
            sock.connect(('example.com', 80))
        except BlockingIOError:
            pass
            # print('非阻塞连接')

        f = Future()

        def on_connected():
            f.set_result(None)

        selector.register(sock.fileno(), EVENT_WRITE, on_connected)
        # 返回f对象，当连接成功时会调用f对象
        yield f

        selector.unregister(sock.fileno())
        get = f'GET {self.url} HTTP/1.0\r\nHOST: example.com\r\n\r\n'
        sock.send(get.encode('ascii'))

        global stopped, urls_todo

        while True:
            f = Future()
            def on_readable():
                f.set_result(sock.recv(4096))
            selector.register(sock.fileno(), EVENT_READ, on_readable)
            chunk = yield f
            if chunk:
                self.response += chunk
            else:
                selector.unregister(sock.fileno())
                urls_todo.remove(self.url)
                if not urls_todo:
                    stopped = True
                break



if __name__ == '__main__':
    import time

    s1 = time.time()
    for url in urls_todo:
        c = Crawler(url)
        c.fetch()
    print(time.time() - s1)

