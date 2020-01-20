# 罗马数字
dic = {'I': 1, 'V': 5, 'X': 10, 'L': 50,
'C': 100, 'D': 500, 'M': 1000, 'IV':4, 'IX':9,
'XL':40, 'XC':90, 'CD':400, 'CM':900}

def func(s):
    num = 0
    flag = True
    s_array = [_ for _ in s]
    count = len(s_array)
    for i in range(count):
        if flag:
            s = s_array[i]
            if s in ['I', 'X', 'C'] and i+1<count:
                ss = s_array[i] + s_array[i+1]
                if ss in dic:
                    num+=dic[ss]
                    flag = False
                else:
                    num+=dic[s]
            else:
                num+=dic[s]
        else:
            flag = True
    return num

if __name__ == '__main__':
    s = 'MCMXCIV'
    result = func(s)
    print(result)
