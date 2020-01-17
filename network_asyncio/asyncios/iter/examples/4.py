"""
    生成器其实是一种特殊的迭代器，不过这种迭代器更加优雅。
    它不需要再像上面的类一样写__iter__()和__next__()方法了，只需要一个yiled关键字。 生成器一定是迭代器（反之不成立）
    # yield from关键字可以直接返回一个生成器
"""
def func1(Flag=False):
    print('启动生成器')
    count = 1
    while True:
        num = yield count
        print('获取num', num)
        count += num
        if Flag and count > 10:
            break
    return 'gave over'

def test1():
    # 生成器简单实例
    f1 = func1()
    print(f'f1是一个生成器:{f1}')
    # next等价于f1.send(None)，启动生成器
    next(f1)
    count = f1.send(2)
    print('获取count', count)

def func2():
    print('启动生成器2')
    count = []
    while True:
        # yield from 相当于建立了一条连接，并会出里内层的StopIteration
        value = yield from func1(True)  # 返回会结束的func1生成器
        print(value)
        yield from func1(False) # 返回不会结束的func1生产器

def test2():
    f2 = func2()
    print(f'f2是一个生成器:{f2}')
    next(f2)
    count = 1
    while True:
        value = f2.send(count)
        print(value)
        count+=1
        if count == 10:
            break

if __name__ == '__main__':
    test1()
    print()
    test2()
