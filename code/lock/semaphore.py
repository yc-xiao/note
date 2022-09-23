from contextlib import contextmanager
import threading
import redis
import time
import os

redis_obj = redis.Redis(decode_responses=True)

"""
    基于redis实现自旋锁
"""

def unlock_by_redis(key='lock'):
    redis_obj.delete(key)

def lock_by_redis(key='lock', expire=2, increase=True, R=True):
    """
        使用redis实现自旋锁
            key 设置锁名称
            expire 设置使用锁的时间单位s, 过期自动归还锁
            increase 设置抢锁时间是否递增(0.1~0.5)，默认开启
            R 设置是否允许多次/递归调用
    """
    sleep_time = 0.1
    value = f'{os.getpid()}-{threading.get_ident()}' if R else 1
    # 当key不存在时，存入key值。即第一个线程可以获取锁，并设置过期时间。
    # 后面的线程只能等锁释放或锁过期后再获取锁并设置过期时间
    while not redis_obj.set(key, value, ex=expire, nx=True):
        # 当R为True时，判断key与value是否一致，而redis获取的value可能是未处理的字符或已处理的字符串
        if R and redis_obj.get(key) in (value, value.encode()):
            break
        time.sleep(sleep_time)
        if increase:
            sleep_time = sleep_time * 2
            if sleep_time > 0.5:
                sleep_time = 0.5

@contextmanager
def lock_redis(key='lock', expire=2, increase=True, R=True):
    """
        # 支持多进程多线程，可通过expire参数设置取锁时间
        with lock_redis():
            func() # 执行函数
    """
    try:
        yield lock_by_redis(key, expire=expire, increase=increase, R=R)
    except Exception as e:
        raise e
    finally:
        unlock_by_redis(key)

"""
    基于redis实现信号量
"""

class SemaphoreRedis:
    def __init__(self, redis_obj=None, name='s', n=1, expire=60, auto_delete=True):
        """
            说明:
                该类基于Redis库, redis_obj为redis库的实例
                name为信号量名，同时作为redis_obj操作的key
                n为可用资源的值，当n=1时，可做为互斥锁，当n=2时，表示可并发使用两个资源
                expire=60s，给信号量设置过期时间，预防死锁
                auto_delete，控制__del__函数回收
            PS: 在多线程/多进程情况下，多次初始化SemaphoreRedis，当name，redis_obj值相同时则认为是同一个信号量。N值在首次创建生效。
        """
        self.redis_obj = redis_obj
        self.name = name

        # 多次初始化SemaphoreRedis，仅第一次设置n值，N与NK记录全局的n字段
        self.N, self.NK = 0, f'{name}-N-KEY'
        self.redis_obj.set(name, n, nx=True)
        self.redis_obj.set(self.NK, n, nx=True)
        
        # 记录实例个数，当__del__时判断是否有存活的实例
        self.auto_delete = auto_delete
        self.All = f'{name}-All-instance'        
        self.redis_obj.incr(self.All)

        # 设置过期时间
        self.expire(expire)

    def __del__(self):
        if self.auto_delete and self.redis_obj.decr(self.All) <= 0:
            self.destroy()

    def _decr(self):
        return self.redis_obj.decr(self.name)
    
    def _incr(self):
        return self.redis_obj.incr(self.name)

    def _sleep(self, sec):
        # 多次加锁，等待时间从0.1递增到0.5
        time.sleep(sec)
        sec = sec * 2
        return sec if sec <= 0.5 else 0.5

    def _get_N(self):
        if not self.N:
            n = self.redis_obj.get(self.NK) or '0'
            self.N = int(n)
        return self.N

    def destroy(self):
        # 手动销毁
        self.redis_obj.delete(self.All)
        self.redis_obj.delete(self.NK)
        self.redis_obj.delete(self.name)

    def expire(self, sec):
        # 设置过期时间
        self.redis_obj.expire(self.name, sec)
        self.redis_obj.expire(self.NK, sec)
        self.redis_obj.expire(self.All, sec)
    
    def P(self):
        # 信号量-1<0，等待
        sleep_time = 0.1
        while self._decr() < 0 :
            self._incr()
            sleep_time = self._sleep(sleep_time)

    def V(self):
        # 信号量+1>N，等待
        sleep_time = 0.1
        while self._incr() > self._get_N():
            self._decr()
            sleep_time = self._sleep(sleep_time)

    @contextmanager
    def lock(self):
        try:
            yield self.P()
        except Exception as e:
            raise e
        finally:
            self.V()