
import asyncio
import time

async def sleep(i):
    print(i)
    await asyncio.sleep(i)


async def main():
    tasks = [asyncio.create_task(sleep(i)) for i in range(3)]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    s1 = time.time()
    asyncio.run(main())
    print(time.time()-s1)
