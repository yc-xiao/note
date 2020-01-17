'''
    协程又程微线程。
    多线程编程:一个进程多个线程，由操作系统(内核态)进行多线程切换以及上下文(栈，寄存器)保存。
    协程:一个进程一个线程可完成，由代码(用户态)进行多协程切换，相对于系统操作，节省大量资源。
    在python中，协程通过generator，生成对象处理。
    协程不需要加锁，原因是而非线程的抢占式多任务，协程执行的任务只要逻辑上保证原子性的(就跟加了锁一样happy)。
    协程是由代码控制，一般是原子性的，有序执行。多线程执行算法存在抢占式，导致数据不一致。
'''

def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'

def produce(c):
    c.send(None)
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()

c = consumer()　#　返回是一个对象，不是单纯的函数调用
produce(c)

# 伪代码
# class Generator(object):
#     def __init__(self, name, func):
#         self.name = name
#         self.func = func
#
#     def run(self, *args, **kw):
#         result = self.func(*args, **kw)
#         return result
#
#     def __iter__(self):
#         return self
#
#     def __next__(self, index=0):
#         if index == 0:
#             result = self.run()
#             return result
#         raise StopIteration
#
#     def __call__(self, gobj):
#         next(self.run)
#
# c = Generator('消费者', func=None)
# p = Generator('生产者', func=None)
# p(c)
