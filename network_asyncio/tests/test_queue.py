from __init__  import *
from threading_pool.oqueue import ThreadSafeQueue

import threading
import random
import time


def consumer(queue, sleep):
    while True:
        num = queue.pop()
        print('consumer:', num)
        queue.pp()
        time.sleep(sleep)

def producer(queue, sleep):
    while True:
        num = random.randint(10, 1000)
        queue.put(num)
        print('producer', num)
        time.sleep(sleep)

def sort(queue, sleep):
    while True:
        queue.sort(func=sorted)
        time.sleep(sleep)

def exce_ths(ths):
    for th in ths:
        th.start()
    for th in ths:
        th.join()

def test_c_p():
    # 当生产者快于消费者
    print('生产者快于消费者')
    queue = ThreadSafeQueue(10)
    tc = threading.Thread(target=consumer, args=(queue, 10))
    tp = threading.Thread(target=producer, args=(queue, 3))
    exce_ths([tc, tp])

def test_p_c():
    # 当消费者快于生产者
    print('消费者快于生产者')
    queue = ThreadSafeQueue(10)
    tc = threading.Thread(target=consumer, args=(queue, 3))
    tp = threading.Thread(target=producer, args=(queue, 10))
    exce_ths([tc, tp])


def test_sort():
    '''
        排序存在一个问题，假设排序完成后有新的数据添加。
        在获取时还是取得新加入的排序，导致排序错误
    '''
    print('测试队列排序')
    queue = ThreadSafeQueue(10)
    tp = threading.Thread(target=producer, args=(queue, 2))
    tc = threading.Thread(target=consumer, args=(queue, 5))
    ts = threading.Thread(target=sort, args=(queue, 10))
    exce_ths([tc, tp, ts])

def main():
    # test_c_p()
    # test_p_c()
    test_sort()

if __name__ == '__main__':
    main()
