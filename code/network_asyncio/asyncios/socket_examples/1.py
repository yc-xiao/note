"""
    单线程阻塞
    https://www.ctolib.com/topics-121825.html
"""
import socket
import time


def blocking_way():
    sock = socket.socket()
    # blocking
    sock.connect(('example.com', 80))
    request = 'GET / HTTP/1.0\r\nHOST: example.com\r\n\r\n'
    sock.send(request.encode('ascii'))
    response = b''
    chunk = sock.recv(4096)
    while chunk:
        response += chunk
        # blocking
        chunk = sock.recv(4096)
    return response


def sync_way():
    res = []
    for i in range(10):
        res.append(blocking_way())
    print(res)
    return len(res)


if __name__ == '__main__':
    t1 = time.time()
    sync_way()
    t2 = time.time()
    print(t2-t1)