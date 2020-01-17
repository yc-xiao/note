"""
    await　可以等待三种对象，协程，任务，未来对象。
        await　等待返回结果，同时会释放cpu使用权，进行事件循环执行其他任务。当前协程会卡在await。

        调用协程，返回一个协程对象，不会立刻执行。需要放到事件循环执行。
        任务，对协程的封装，会在内部添加到事件循环中。
        future，对任务进行封装，可以查询任务的执行情况。
"""
import asyncio
import time

async def main():
    coroutine = asyncio.sleep(2)
    coroutine2 = asyncio.sleep(3)
    print(coroutine)
    result = await coroutine

# 异步，必须接收一个携程，携程内部可以调用其他携程或同步代码
s1 = time.time()
asyncio.run(main())
print(time.time()-s1)
