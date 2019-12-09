# 判断一个数是不是回文
def is_hw(array):
    count = len(array)
    num = count//2
    for i in range(num):
        if array[i] != array[count-i-1]:
            return False
    return True
