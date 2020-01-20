
def cal(a, b):
    result = ''
    la = len(a)
    lb = len(b)
    f = False
    for i in range(la):
        va = a[i]
        vb = b[i] if i<lb else '0'
        if va == '1' and vb == '1':
            s = '1' if f else '0'
            f = True
        elif va == '0' and vb == '0':
            s = '1' if f else '0'
            f = False
        else:
            s = '0' if f else '1'
        result+=s
    if f:
        result+='1'
    return result

def func(a, b):
    _a = a[::-1]
    _b = b[::-1]
    result = cal(_a,_b) if len(a)>len(b) else cal(_b,_a)
    return result[::-1]

if __name__ == '__main__':
    a = "11"
    b = "11"
    result = func(a, b)
    print(result)
