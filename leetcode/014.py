
def cmp(cmp1, cmp2):
    result = []
    l1 = len(cmp1)
    l2 = len(cmp2)
    ll = l1 if l1 < l2 else l2
    for i in range(ll):
        if cmp1[i] == cmp2[i]:
            result.append(cmp1[i])
        else:
            return result
    return result

def func(datas):
    count = len(datas)
    result = ''
    if count==0:
        return ''
    elif count==1:
        return datas[0]
    else:
        cmp1 = [_ for _ in datas.pop()]
        for data in datas:
            data = [_ for _ in data]
            cmp1 = cmp(data, cmp1)
            if not cmp1:
                return ''
        return ''.join(cmp1)

if __name__ == '__main__':
    datas = ["flower","flow","flight"]
    # datas = ["dog","racecar","car"]
    result = func(datas)
    print(result)
