from task import Task
from pool import Pool
import time

def process():
    print('this is a simple task')

def test():
    # 1.初始化线程池
    pool = Pool(4)
    pool.start()
    # 2.添加任务
    for i in range(10):
        task = Task(func=process)
        # 3.执行任务
        pool.put(task)
    pool.join()

if __name__ == '__main__':
    test()
