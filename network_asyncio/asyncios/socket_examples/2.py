"""
    单线程非阻塞
"""
import socket
import time


def send(sock, request):
    while True:
        try:
            sock.send(request.encode('ascii'))
            break
        except:
            pass
            # print('发送非阻塞，会立刻返回一个错误')


def recv(sock):
    while True:
        try:
            chunk = sock.recv(4096)
            return chunk
        except:
            pass
            # print('读取非阻塞，会立刻返回一个错误')


def blocking_way():
    sock = socket.socket()
    sock.setblocking(False)
    try:
        sock.connect(('example.com', 80))
    except:
        # print('连接非阻塞,会立刻返回一个错误')
        pass
    request = 'GET / HTTP/1.0\r\nHOST: example.com\r\n\r\n'
    send(sock, request)

    response = b''
    chunk = recv(sock)
    while chunk:
        response += chunk
        chunk = recv(sock)
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
    print('虽然非阻塞，但是需要占用cpu不断询问结果')