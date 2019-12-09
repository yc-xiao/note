from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED
from functools import wraps
import threading
import requests
import time
url = 'http://49.234.194.213/'
req_results = []

def res_func(url):
    # print(url)
    res = requests.get(url)
    req_results.append(res.status_code)

def pp(func):
    @wraps(func)
    def inner(*args, **kw):
        start_time = time.time()
        result = func(*args, **kw)
        end_time = time.time()
        print(f'{func.__name__}运行时间:{end_time-start_time}s')
        return result
    return inner

@pp
def request_line_func():
    for i in range(20):
        res_func(url)

@pp
def request_supervene_func():
    pool = ThreadPoolExecutor(8)
    result = [pool.submit(res_func, url) for i in range(2000)]
    pool.shutdown()
    wait(result, return_when=ALL_COMPLETED)
    print(len(req_results))

if __name__ == '__main__':
    # request_line_func()
    request_supervene_func()
