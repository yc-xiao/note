
import asyncio, aiohttp
import time

num = 800
url = 'http://127.0.0.1:5000/test_thread/post/1'

async def req():
    results = []
    async with aiohttp.ClientSession() as session:
        for i in range(num):
            # 如果只有req单个任务，那没有异步效果，即使异步了，异步期间没有其他任务依旧await等待
            async with session.get(url) as response:
                result = await response.read()
                print(result)
            results.append(result)
    return results

async def req2():
    # 异步任务
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result = await response.read()
            print(result)
            return result

async def main():
    task1 = asyncio.create_task(req())
    task2 = asyncio.create_task(req())
    # 两个任务并发
    await task1
    await task2
    # results = await asyncio.gather(*tasks)

async def main2():
    # 多个任务并发
    # await asyncio.gather(*[req2() for i in range(num)])
    tasks = [asyncio.create_task(req2()) for i in range(num)]
    results = await asyncio.gather(*tasks)
    print(len(results))

def test():
    # 单线程非异步
    import requests
    for i in range(num):
        requests.get(url)


if __name__ == '__main__':
    t1 = time.time()
    asyncio.run(main2())
    # asyncio.run(main())
    # test()
    t2 = time.time()
    print(t2-t1)
