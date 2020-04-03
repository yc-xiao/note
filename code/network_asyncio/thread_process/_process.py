from multiprocessing import Process
from base import cal_x, cal_t

@cal_t
def test_func():
    ts = []
    for i in range(6):
        t1 = Process(name=i, target=cal_x, args=(10,))
        t1.daemon = True # 主线程死亡，该线程也死亡
        t1.start() # t1.run() 直接执行cal，t1.start() 启动一个线程
        ts.append(t1)
    for t in ts:
        t.join() # 主线程是否等待子线程


if __name__ == '__main__':
    test_func()
