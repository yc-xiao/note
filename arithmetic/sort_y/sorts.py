'''
    插入排序 (适合有序排序) O(n)-n**2，对近乎有序的排序，速度能达到O(n)
    希尔排序 (插入排序改良版，修改大规模无序数组)
    并归排序 nO(log2n)
    快速排序 nO(log2n)
'''
from functools import wraps
import random
import copy
import time


def ptime(func):
    @wraps(func)
    def inner(*args, **kw):
        s1= time.time()
        result = func(*args, **kw)
        s2 = time.time()
        # print(result)
        print(func.__name__, (s2-s1))
        print()
        return result
    return inner

# 插入排序, 每次都需要做交换操作
@ptime
def insert(array):
    array = copy.deepcopy(array)
    for i in range(1, len(array)):
        while i > 0 and array[i] < array[i-1]:
            temp = array[i-1]
            array[i-1] = array[i]
            array[i] = temp
            i -= 1
    return array


# 插入排序, 先移动最后交换
@ptime
def insert2(array):
    array = copy.deepcopy(array)
    for i in range(1, len(array)):
        temp = array[i] # 先记录当前值
        while i > 0 and temp < array[i-1]:
            array[i] = array[i-1]
            i -= 1
        array[i] = temp
    return array

# 用于其他排序调用
def insert3(array):
    array = copy.deepcopy(array)
    for i in range(1, len(array)):
        temp = array[i] # 先记录当前值
        while i > 0 and temp < array[i-1]:
            array[i] = array[i-1]
            i -= 1
        array[i] = temp
    return array

def __merge_sort(array):
    count = len(array)
    if count == 1:
        return array
    larray = __merge_sort(array[:count//2])
    rarray = __merge_sort(array[count//2:])
    _array = []
    l=r=0
    lcount = len(larray)
    rcount = len(rarray)
    for i in range(count):
        if l >= lcount:
            _array.append(rarray[r])
            r+=1
        elif r >= rcount:
            _array.append(larray[l])
            l+=1
        elif larray[l] > rarray[r]:
            _array.append(rarray[r])
            r+=1
        else:
            _array.append(larray[l])
            l+=1
    return _array

def __merge_sort2(array):
    count = len(array)
    if count == 1:
        return array
    if count < 20:
        return insert3(array)
    larray = __merge_sort2(array[:count//2])
    rarray = __merge_sort2(array[count//2:])
    _array = []
    l=r=0
    lcount = len(larray)
    rcount = len(rarray)
    for i in range(count):
        if l >= lcount:
            _array.append(rarray[r])
            r+=1
        elif r >= rcount:
            _array.append(larray[l])
            l+=1
        elif larray[l] > rarray[r]:
            _array.append(rarray[r])
            r+=1
        else:
            _array.append(larray[l])
            l+=1
    return _array

# 归并排序
@ptime
def merge_sort(array):
    return __merge_sort(array)

# 归并排序
@ptime
def merge_sort2(array):
    return __merge_sort2(array)

if __name__ == '__main__':
    array = [random.randint(0, 3) for i in range(10000)]
    # array = [random.randint(0, 1000) for i in range(10000)]
    # print(array)
    print()
    # insert(array)
    # insert2(array)
    array_m = copy.deepcopy(array)
    merge_sort(array_m)
    array_m2 = copy.deepcopy(array)
    merge_sort2(array_m2)
