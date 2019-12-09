import time
import asyncio


now = lambda : time.time()


async def do_some_work(x):
    print("waiting:", x)

start = now()
# 这里是一个协程对象，这个时候do_some_work函数并没有执行
coroutine = do_some_work(2)
print(coroutine)
#  创建一个事件loop
loop = asyncio.get_event_loop()
# 将协程加入到事件循环loop
loop.run_until_complete(coroutine)

print("Time:",now()-start)
