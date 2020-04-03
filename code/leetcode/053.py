def max(result):
    max = result[0]
    for each in result:
        if each > max:
            max = each
    return max

def func(nums):
    result = []
    value = -10000
    for each in nums:
        if each >= 0:
            if value < 0:
                value = each
            else:
                value+=each
        else:
            if value < each:
                value = each
            else:
                temp_value = value + each
                if temp_value < 0:
                    value = each
                else:
                    value = temp_value
        result.append(value)
    return result

if __name__ == '__main__':
    nums = [-2,1,-3,4,-1,2,1,-5,4]
    result = func(nums)
    v = max(result)
    print(result, v)
