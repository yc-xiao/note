import time
import asyncio
from aiohttp import ClientSession

tasks = []
url = "http://49.234.194.213"
async def hello(url):
    async with ClientSession() as session:
        async with session.get(url) as response:
#            print(response)
            # print('Hello World:%s' % time.time())
            await response.read()
            return 1

def run():
    for i in range(100):
        task = asyncio.ensure_future(hello(url.format(i)))
        tasks.append(task)
    result = loop.run_until_complete(asyncio.gather(*tasks))
    print(result)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    run()
