'''
    协程运行方式:并发执行，新建任务并发。
    asyncio.create_task 新增的任务，会自动添加到执行队列。任务是一个对象，会记录执行状态。
'''
import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    task1 = asyncio.create_task(
        say_after(1, 'hello'))

    task2 = asyncio.create_task(
        say_after(2, 'world'))

    print(f"started at {time.strftime('%X')}")

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    await task2
    await task1
    # asyncio.create_task 新增的任务，会自动添加到执行队列
    # await asyncio.sleep(12)

    print(f"finished at {time.strftime('%X')}")
asyncio.run(main())
