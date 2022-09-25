
from multiprocessing import Process
from threading import Thread
from semaphore import SemaphoreRedis, lock_redis, redis_obj
import time

def test_multiprocessing(func, num=5):
    start = time.time()
    print(f'start test multiprocessing func -> {func.__name__}')
    ps = []
    for i in range(num):
        p = Process(target=func, args=(f'p{i+1}',))
        p.start()
        ps.append(p)
    for i in range(num):
        ps[i].join()
    print(f'finish test multiprocessing func -> {func.__name__}')
    print(f'all time:{time.time() - start}s')
    print()

def test_threads(func, num=5):
    start = time.time()
    print(f'start test threads func -> {func.__name__}')
    ts = []
    for i in range(num):
        t = Thread(target=func, args=(f'th{i+1}',))
        t.start()
        ts.append(t)
    for i in range(num):
        ts[i].join()
    print(f'finish test threads func -> {func.__name__}')
    print(f'all time:{time.time() - start}s')
    print()

# 多线程多进程，不加锁执行
def test_not_lock(N=5, work_time=1):
    def not_lock(text='ok'):
        time.sleep(work_time)   
        print(text)
    test_threads(func=not_lock, num=N)
    test_multiprocessing(func=not_lock, num=N)

# 多线程多进程，测试互斥锁
def test_with_lock(N=5, work_time=1):
    def with_lock(text='ok'):
        with lock_redis(expire=10):
            time.sleep(work_time) # 模拟工作
            print(text)
    test_threads(func=with_lock, num=N)
    test_multiprocessing(func=with_lock, num=N)

# 多线程多进程，测试互斥R锁
def test_with_r_lock(N=5, work_time=2):
    def with_r_lock(text='ok'):
        key, R, increase = 'aa', True, False
        with lock_redis(key=key, expire=10, R=R, increase=increase):
            with lock_redis(key=key, expire=10, R=R, increase=increase):
                time.sleep(work_time) # 模拟工作
        print(text)
    test_threads(func=with_r_lock, num=N)
    test_multiprocessing(func=with_r_lock, num=N)

# 多线程多进程，测试单个信号量
def test_semaphore_lock(N=5, work_time=1):
    def semaphore_lock(text='ok'):
        s = SemaphoreRedis(redis_obj=redis_obj, expire=30)
        with s.lock():
            time.sleep(work_time)
            print(text)
    test_threads(func=semaphore_lock, num=N)
    test_multiprocessing(func=semaphore_lock, num=N)

# 多线程多进程，测试多个信号量
def test_semaphore_N_lock(N=5, work_time=1):
    def semaphore_N_lock(text='ok'):
        s = SemaphoreRedis(redis_obj=redis_obj, n=3)
        with s.lock():
            time.sleep(work_time)
            print(text)
    test_threads(func=semaphore_N_lock, num=N)
    test_multiprocessing(func=semaphore_N_lock, num=N)


def test():
    test_not_lock()
    test_with_lock()
    test_with_r_lock()
    test_semaphore_lock()
    test_semaphore_N_lock()
    return

if __name__ == '__main__':
    # test_with_lock(work_time=0.1)
    # test_with_r_lock(work_time=0.1)
    pass