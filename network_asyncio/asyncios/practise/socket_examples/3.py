"""
    询问操作交给OS
"""
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ
import socket

selector = DefaultSelector()
stopped = False
urls_todo = {'/', '/1', '/2', '/3', '/4', '/5', '/6', '/7', '/8', '/9'}


class Crawler:
    def __init__(self, url):
        self.url = url
        self.sock = None
        self.response = b''

    def fetch(self):
        self.sock = socket.socket()
        # 设置非阻塞
        self.sock.setblocking(False)
        try:
            self.sock.connect(('example.com', 80))
        except BlockingIOError:
            pass
            # print('非阻塞连接')
        selector.register(self.sock.fileno(), EVENT_WRITE, self.connected)

    def connected(self, key, mask):
        get = f'GET {self.url} HTTP/1.0\r\nHOST: example.com\r\n\r\n'
        self.sock.send(get.encode('ascii'))
        selector.unregister(key.fd)
        selector.register(key.fd, EVENT_READ, self.read_response)

    def read_response(self, key, mask):
        global stopped, urls_todo
        chunk = self.sock.recv(4096)
        # 如果响应很大的时候,处于监听状态会重复调read_response
        if chunk:
            self.response += chunk
        else:
            selector.unregister(key.fd)
            urls_todo.remove(self.url)
            if not urls_todo:
                stopped = True


def loop():
    while not stopped:
        events = selector.select()
        print(events)
        for event_key, event_mask in events:
            callback = event_key.data
            callback(event_key, event_mask)


if __name__ == '__main__':
    import time
    s1 = time.time()
    for url in urls_todo:
        c = Crawler(url)
        c.fetch()
    loop()
    print(time.time()-s1)

"""
    from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ
    import socket
    
    #　1.创建一个事件监听对象
    selector = DefaultSelector() 
    
    # 2.创建非阻塞socker，并将socker注册到selector, self.connected为可写事件就绪后执行的回调函数
    self.sock = socket.socket()
    sock.setblocking(False)
    try:
        sock.conn()
    except BlockingIOError:
        pass
    selector.register(sock.fileno(), EVENT_WRITE, self.connected)
    
    # 3.执行回调函数，同时取消注册
    # 4.由于以上都是非阻塞，一下就ok了，那接下来是进行循环监听事件loop
    
"""