
def func(s):
    i = 0
    _s = ' '
    for _ in s[::-1]:
        if _ == _s and not i:
            continue
        if _ == _s:
            break
        i+=1
    return i

if __name__ == '__main__':
    s = "Hello World"
    result = func(s)
    print(result)
