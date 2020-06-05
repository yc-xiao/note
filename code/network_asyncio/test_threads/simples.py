import threading

lock = threading.Lock()

ss = threading.Semaphore(1)

def _func():
    print('3')
    for i in range(5):
        print(i, end=' ')
    print()
    print('4')

def func():
    with ss:
        _func()

def main():
    ths = [threading.Thread(target=func) for i in range(10)]
    [th.start() for th in ths]
    [th.join() for th in ths]


if __name__ == '__main__':
    main()
