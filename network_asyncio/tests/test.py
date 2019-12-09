from functools import wraps
import threading
import unittest

def pp(func):
    @wraps(func)
    def inner(*args, **kw):
        print('')
        result = func(*args, **kw)
        print('')
        return result
    return inner

class TestThreadSafeQueue(unittest.TestCase):
    @pp
    def tearDown(self):
        # 每个测试用例执行之后做操作
        print('test end')

    @pp
    def setUp(self):
        # 每个测试用例执行之前做操作
        print('test start')

    @classmethod
    @pp
    def tearDownClass(self):
    # 必须使用 @ classmethod装饰器, 所有test运行完后运行一次
        print('game over')

    @classmethod
    @pp
    def setUpClass(self):
    # 必须使用@classmethod 装饰器,所有test运行前运行一次
        self.queue = ThreadSafeQueue()
        print('game start')


    def test_more_thread(self):
        self.assertEqual(1, 1)  # 测试用例

if __name__ == '__main__':
    unittest.main()#运行所有的测试用例
