from __init__  import *
from threading_pool.opool import ThreadPool, Task
from functools import wraps
import requests
import time


req_results = []

def res_func(url):
    res = requests.get(url)
    req_results.append(res.status_code)

def cal_num():
    count = 1
    for i in range(100000):
        count += i
    return count

def exce_time(func):
    @wraps(func)
    def inner(*args, **kw):
        start = time.time()
        result = func(*args, **kw)
        end = time.time()
        print(f'{func.__name__}执行时间为:', end-start)
        return result
    return inner

def test_tread_pool():
    pool = ThreadPool()
    url = 'http://49.234.194.213/'
    tasks = [Task(func=cal_num, desc='test') for i in range(100)]
    # tasks = [Task(func=res_func, desc='request', args=(url, )) for i in range(100)]
    pool.batch_put_task(tasks) # 批量添加任务
    pool.start()    # 启动线程池
    pool.is_ko()    # 等待任务完成
    pool.batch_put_task_and_console_thread(tasks) # 重新添加任务
    pool.is_ko()    # 等待任务完成
    pool.stop()     # 关闭线程池 close()

@exce_time
def main():
    test_tread_pool()

if __name__ == '__main__':
    main()
