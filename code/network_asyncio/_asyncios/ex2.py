"""
    yield
    yield from 迭代一个循环
"""

def g1():
    yield 'g1'
    yield [i for i in range(10)]

def g2():
    yield from 'g2'
    yield from [i for i in range(10)]

for _ in g1():
    print(_)

print('*'*30)

for _ in g2():
    print(_)
