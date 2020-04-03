import threading

num = 0
_lock = threading.Lock()

def add_num(lock=False):
    global num
    for i in range(100000):
        if lock:
            _lock.acquire()
        num += 1
        if lock:
            _lock.release()

def reduce_num(lock=False):
    global num
    for i in range(100000):
        if lock:
            _lock.acquire()
        num -= 1
        if lock:
            _lock.release()

def func(lock=False):
    global num
    num = 0
    th_a = threading.Thread(target=add_num, args=(lock,))
    th_r = threading.Thread(target=reduce_num, args=(lock,))
    th_a.start()
    th_r.start()
    th_a.join()
    th_r.join()
    print(f'lock:{lock},num的值为', num)


if __name__ == '__main__':
    func()
    func(True) #加锁
