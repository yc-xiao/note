#coding:utf-8
import time,asyncio,aiohttp


url = 'http://49.234.194.213'
async def hello(url,semaphore):
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.read()


async def run():
    semaphore = asyncio.Semaphore(2) # 限制并发量为500
    to_get = [hello(url.format(),semaphore) for _ in range(10000)] #总共1000任务
    await asyncio.wait(to_get)


if __name__ == '__main__':
#    now=lambda :time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.close()
