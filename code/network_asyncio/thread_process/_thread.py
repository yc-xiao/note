from base import cal_x, cal_t
import threading

@cal_t
def test_func():
    ts = []
    for i in range(6):
        t1 = threading.Thread(name=i, target=cal_x)
        t1.daemon = True # 主线程死亡，该线程也死亡
        ts.append(t1)
        t1.start() # t1.run() 直接执行cal，t1.start() 启动一个线程
    for t in ts:
        t.join() # 主线程是否等待子线程

if __name__ == '__main__':
    test_func()
