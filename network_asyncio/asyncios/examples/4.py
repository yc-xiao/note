import asyncio
from aiohttp import ClientSession


tasks = []
url = "http://49.234.194.213"
async def hello(url):
    async with ClientSession() as session:
        async with session.get(url) as response:
            response = await response.read()


def main(loop):
    tasks = []
    for i in range(100):
        # func(url)
        tasks.append(hello(url))
    loop.run_until_complete(asyncio.gather(*tasks))
        # async with ClientSession() as session:
        #     async with session.get(url) as response:
        #         response = await response.read()
        #         print(2)

import requests
def func(url):
    requests.get(url)

if __name__ == '__main__':
    import time
    s1 = time.time()
    loop = asyncio.get_event_loop()
    main(loop)
    s2 = time.time()
    print(s2-s1)
