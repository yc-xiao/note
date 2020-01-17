"""
for语句的原理就是先用iter函数获取可迭代对象的迭代器，然后调用next函数。
此函数自动调用迭代器对象的next方法，每次遍历都返回相应的值，如果没有返回值了，就会抛出StopIter异常for语句自动捕获异常并处理
"""

# 可迭代对象，可调用iter()并返回一个迭代器
class CIterable(object):
    def __iter__(self):
        return CIterator()

# 实现next()，称为迭代器
class CIterator(object):
    # __next__ 需要实现StopIteration退出迭代
    def __next__(self):
        print('start')
        raise StopIteration

class CIterable2(CIterable):
    def __init__(self, count=10):
        self.count = count
    def __iter__(self):
        return CIterator2(self.count)

class CIterator2(CIterator):
    def __init__(self, count):
        self.count = count
        self.index = 0

    def __next__(self):
        print('start', self.index)
        if self.index < self.count:
            self.index += 1
            return self.index
        raise StopIteration

def test1():
    citerable = CIterable()
    citerator = iter(citerable)
    print(citerator)
    for i in citerable:
        print(i)

def test2():
    citerable = CIterable2()
    citerator = iter(citerable)
    print(citerator)
    for i in citerable:
        print(i)

if __name__ == '__main__':
    test1()
    print()
    test2()
