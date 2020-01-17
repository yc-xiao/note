"""
    生成器其实是一种特殊的迭代器，不过这种迭代器更加优雅。
    它不需要再像上面的类一样写__iter__()和__next__()方法了，只需要一个yiled关键字。 生成器一定是迭代器（反之不成立）
"""


def func():
    print('start')
    count = 0
    while True:
        num = yield count
        print('num', num)
        if isinstance(num, int):
            count += num
        else:
            count += 1

if __name__ == '__main__':
    f = func()
    print(f)
    print(dir(f))
    print(f.send(None))
    print()
    print(f.send(2))
    print()
    print(f.send(111))
