import threading
import socket
import random
import time
import pdb

def view(msg, conn, tt, app):
    # 必须按照http协议的格式，才能在浏览器正常显示
    # 返回数据长度要正确
    # time.sleep(tt)
    print(tt, msg, conn)
    import pdb;pdb.set_trace()
    conn.send(b'HTTP/1.0 200 OK\r\n')
    conn.send(b'Content-Type: text/plain; charset=utf-8\r\n')
    msg = app(conn,'')
    conn.send(b'Content-Length: %d\r\n\r\n' % len(msg))
    conn.send(msg)
    print(tt, msg, conn)
    conn.close()


def application(env, start_response):
    return b'helloc'

def main(app):
    st = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    st.bind(('127.0.0.1', 8888))
    st.listen(10)
    while True:
        try:
            conn, addr = st.accept()
            msg = b'helloc\r\n'
            data = {
                'msg': msg,
                'conn': conn,
                'tt': random.randint(19,20),
                'app': app
            }
            # 通过多线程处理多个连接
            th = threading.Thread(target=view, kwargs=data)
            th.setDaemon(True)
            th.start()
        except KeyError:
            break
    st.close()


if __name__ == '__main__':
    main(application)
