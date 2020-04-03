

def func(s):
    cmp = {')':'(', ']':'[', '}':'{'}
    temps = ['(', '[', '{']
    result = []
    for _ in s:
        if not _:
            continue
        if _ in temps:
            result.append(_)
        else:
            if result.pop() != cmp[_]:
                return False
    return True



if __name__ == '__main__':
    s='{()[]{}{}{}]}'
    result = func(s)
    print(result)
