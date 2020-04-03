# 字符串转为整数
import pdb
def myAtoi(str):
    flag = 0
    str = str.strip()
    nums = []
    for each in str:
        if each == '-' or each == '+':
            if flag or len(nums):
                break
            flag = -1 if each == '-' else 1
            continue
        if not each.isdigit():
            break
        nums.append(each)
    if not nums:
        num = 0
    else:
        num = int(''.join(nums))
    if flag:
        num = num * flag
    if num > 2**31 -1:
        return 2**31-1
    if num < -2**31:
        return -2**31
    return num

if __name__ == '__main__':
    tests = ["42", "   -42", "4193 3with words", "words and 987", "-91283472332", "0-1"]
    results = [42, -42, 4193, 0, -2147483648, 0]

    for i in range(len(tests)):
        print(myAtoi(tests[i]))
        try:
            assert results[i] == myAtoi(tests[i])
        except Exception as e:
            print(e)
            pdb.set_trace()
            myAtoi(tests[i])
