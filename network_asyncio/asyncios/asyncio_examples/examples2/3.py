import asyncio
import random
import time

async def func(value, delay):
    if value == 3:
        raise Exception('this has a error')
    print('helloa', value, delay)
    await asyncio.sleep(delay)
    print('helloz', value, delay)
    return value

async def main():
    tasks = [func(i, random.randint(0,3)) for i in range(10)]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    print(results)

s1 = time.time()
asyncio.run(main())
print(time.time()-s1)
