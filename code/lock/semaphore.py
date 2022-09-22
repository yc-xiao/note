from contextlib import contextmanager
import redis
import time

redis_obj = redis.Redis()

"""
    基于redis实现自旋锁与信号量
"""

def unlock_by_redis(key='lock'):
    redis_obj.delete(key)

def lock_by_redis(key='lock', expire=2):
    """
        使用redis实现自旋锁
            通过设置过期时间expire=2，预防死锁
            多次拿锁，睡眠时间会从0.1递增到0.5
    """
    sleep_time = 0.1
    while redis_obj.incr(key) !=1:
        time.sleep(sleep_time)
        sleep_time = sleep_time * 2
        if sleep_time > 0.5:
            sleep_time = 0.5
    redis_obj.expire(key, expire)

@contextmanager
def lock_redis(key='lock', expire=2):
    """
        # 支持多进程多线程，可通过expire参数设置取锁时间
        with lock_redis():
            func() # 执行函数
    """
    try:
        yield lock_by_redis(key, expire=expire)
    except Exception as e:
        raise e
    finally:
        unlock_by_redis(key)

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
        # 多次初始化SemaphoreRedis，仅第一次有效，N与NK记录全局的N字段
        self.N = 0
        self.NK = f'{name}-N-KEY'
        
        # 多次初始化，仅设置第一个N值，并记录，nx表示存在则不做操作
        self.redis_obj.set(name, n, nx=True)
        self.redis_obj.set(self.NK, n, nx=True)
        
        # 记录实例个数，当__del__时判断是否有存活的实例
        self.All = f'{name}-All-instance'        
        self.auto_delete = auto_delete
        if auto_delete:
            self.redis_obj.incr(self.All)
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
        if not self.N:
            n = self.redis_obj.get(self.NK) or '0'
            self.N = int(n)

        # 信号量+1>N，等待
        sleep_time = 0.1
        while self._incr() > self.N:
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