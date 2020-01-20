

def func(digits=[]):
    if not digits:
        return []
    result = []
    count = 0
    for each in digits:
        count*=10
        count+=each
    count+=1
    while count:
        v = count%10
        count = count//10
        result.append(v)
    return result[::-1]

if __name__ == '__main__':
    digits = [1,2,9,9]
    result = func(digits)
    print(result)
