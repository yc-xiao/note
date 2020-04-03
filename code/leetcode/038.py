
def func(n):
    if 1<=n<=5:
        result = ['1', '11', '21', '1211', '111221']
        return result[n-1]
    strs = func(n-1)
    result = ''
    count, ss = 0, strs[0]
    for _ in strs:
        if _ == ss:
            count+=1
        else:
            result += str(count)+ss
            ss = _
            count=1
    result += str(count)+ss
    return result

if __name__ == '__main__':
    n = 4
    result = func(n)
    print(result)
