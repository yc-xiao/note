import asyncio

async def sleep():
    print('start sleep')
    await asyncio.sleep(1)
    print('end sleep')

async def main():
    #await 对象有三种主要类型: 协程, 任务 和 Future.
    # 在一个协程内是按顺序进行的，协程会等待时间
    await sleep()
    await sleep()
    print('---------------------------')
    # 任务 被用来设置日程以便 并发 执行协程。
    task1 = asyncio.create_task(sleep())
    task2 = asyncio.create_task(sleep())
    await task1
    await task2

async def gather():
    # 并发执行
    await asyncio.gather(
            main(),
            main(),
            main(),
    )

if __name__ == '__main__':
    # coroutine = main()
    gather = gather()
    asyncio.run(gather) # 当有其他 asyncio 事件循环在同一线程中运行时，此函数不能被调用。
