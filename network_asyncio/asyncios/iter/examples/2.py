"""
    CIter 具有__iter__方法是可迭代对象，具有__next__是迭代器返回是本身，只能进行一次迭代
    CIter2　重写__iter__，返回新的迭代器，可多次迭代。且添加了参数
    test3/4 添加__iter__参数
"""
class CIter(object):
    def __init__(self, count=3):
        self.count = count
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < self.count:
            self.index+=1
            return self.index
        raise StopIteration

class CIter2(CIter):
    def __iter__(self, count=3):
        return CIter2(count)

def test_iter1():
    citer = CIter()
    for i in citer:
        print(i)
    print(citer.index)

def test_iter2():
    citer = CIter2()
    for i in citer:
        print(i)
    print(citer.index)

def test_iter3():
    # 给iter添加参数
    citer = CIter2()
    citer2 = citer.__iter__(2)
    while True:
        try:
            print(next(citer2))
        except StopIteration:
            break
    for i in citer2:
        print(i)

def test_iter4():
    from functools import partial
    # 给iter添加参数
    citer = CIter2()
    iter2 = partial(CIter2.__iter__, count=2)
    citer2 = iter2(citer)
    while True:
        try:
            print(next(citer2))
        except StopIteration:
            break
    for i in citer2:
        print(i)

if __name__ == '__main__':
    test_iter1()
    print()
    test_iter2()
    print()
    test_iter3()
    print()
    test_iter4()
