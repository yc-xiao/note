
import asyncio
import time

def test1():
    i=0
    while True:
        print(1)
        i = yield asyncio.sleep(i)
        if i == 10:
            break
        print('this test1', i)

def test2():
    i=0
    while True:
        i = yield asyncio.sleep(i)
        if i == 10:
            break
        print('this test2', i)

def main():
    t1 = test1()
    t2 = test2()
    t1.send(None)
    t2.send(None)
    i = 1
    while True:
        i+=1
        try:
            t1.send(i)
            t2.send(i)
        except StopIteration:
            break


if __name__ == '__main__':
    s1 = time.time()
    main()
    print(time.time()-s1)
