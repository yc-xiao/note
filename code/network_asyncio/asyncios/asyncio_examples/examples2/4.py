import asyncio
import random
import time

async def func(value, delay):
    print('helloa', value, delay)
    await asyncio.sleep(delay)
    print('helloz', value, delay)
    return value

async def main():
    # task是任务集合，
    tasks = {asyncio.create_task(func(i, random.randint(0,3))) for i in range(10)}
    done, pending = await asyncio.wait(tasks, timeout=0.1)
    # pending可以继续asyncio.wait
    done1, pending1 = await asyncio.wait(pending)
    print(pending)

s1 = time.time()
asyncio.run(main())
print(time.time()-s1)
