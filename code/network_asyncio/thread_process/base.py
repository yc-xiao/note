from functools import wraps
import time

def cal_t(func):
    @wraps(func)
    def inner(*args):
        s1 = time.time()
        result = func(*args)
        s2 = time.time()
        print(s2-s1, result)
        return result
    return inner

n=0

@cal_t
def cal_x(count=1):
    count = count * 10000000
    for i in range(count):
        cal()
    return n

def cal():
    global n
    n+=1
    n-=1

if __name__ == '__main__':
    cal()
