"""
    补充:上下文管理器
        需要实现__enter__与__exit__方法
        with Class() as 会获取__enter__的返回值
    contextmanager 快速实现上下问
"""
from contextlib import contextmanager

class Context(object):
    def __enter__(self):
        print('start')
        return self

    def __exit__(self, *args, **kw):
        print('end')

    def test(self):
        print('test')

    def __call__(self):
        print('call')
        return self

class Context2(Context):
    def __enter__(self):
        print('start2')

@contextmanager
def func():
    print('helloc')
    yield Context
    print('helloc')

if __name__ == '__main__':
    with Context() as cc:
        cc.test()
    print()

    with Context2():
        print('test2')
    print()

    with func() as cc:
        with cc() as c:
            c.test()
    print()

    with func() as cc:
        cc = cc()
        with cc() as c:
            c.test()
