"""
    使用 async function 可以定义一个 异步函数，在async关键字定义的函数中不能出现yield和yield from
    async 实际是将一个生成器变成可迭代对象，await 操作符后面必须跟一个awaitable对象

    import types
    @types.coroutine      # 将一个生成器变成一个awaitable的对象
"""
# import asyncio
import types

@types.coroutine
def func1_test():
    yield '1'

async def func1():
    f1 = func1_test()
    print(f1)
    value = await f1
    # 函数走不到这里，应该没有返回
    print(value)
    return value

def test1():
    coro = func1()
    print(coro)
    ret = coro.send(None)
    print(ret)

if __name__ == '__main__':
    test1()
    print()
