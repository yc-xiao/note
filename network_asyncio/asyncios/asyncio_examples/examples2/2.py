import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)
    return what

async def main():
    print('start')
    # 任务会自动添加到事件队列中，由于没有await，程序不做等待
    task1 = asyncio.create_task(say_after(1, 'helloc1'))
    task2 = asyncio.create_task(say_after(2, 'helloc2'))
    # 此时事件队列有两个任务，执行await，当前程序暂停等待结果，loop执行task1, task2
    # 当taskn遇到await时，执行其他task。如果await的任务有结果了，直接返回
    result1 = await task1
    print('task1')
    result2 = await task2
    print('task1, task2')

    task3 = asyncio.create_task(say_after(3, 'helloc3'))
    task4 = asyncio.create_task(say_after(1, 'helloc4'))
    result3 = await task3
    print('task3')
    result4 = await task4
    print('task4')

    print('end')

s1 = time.time()
asyncio.run(main())
print(time.time()-s1)
