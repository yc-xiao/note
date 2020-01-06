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
        print(result)
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

# 辅助快排闭区间[]
def insert4(array, start, end):
    for i in range(start+1, end+1):
        temp = array[i]
        while i > start and temp < array[i-1]:
            array[i] = array[i-1]
            i -= 1
        array[i] = temp


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
    _array = copy.deepcopy(array)
    return __merge_sort(_array)

# 归并排序
@ptime
def merge_sort2(array):
    _array = copy.deepcopy(array)
    return __merge_sort2(_array)

# array[start, end]
def __so_quick(array, start, end):
    if end-start < 15:
        return insert4(array, start, end)
    if end <= start:
        return
    # 随机取一个数进行分割
    value = array[start]
    lt_index = start + 1
    gt_index = end
    # 当两者相遇时
    while lt_index < gt_index:
        while lt_index < gt_index and array[lt_index] <= value:
            lt_index += 1
        while lt_index < gt_index and array[gt_index] >= value:
            gt_index -= 1

        if lt_index < gt_index:
            temp = array[lt_index]
            array[lt_index] = array[gt_index]
            array[gt_index] = temp
            lt_index += 1
            gt_index -= 1

    if array[lt_index] > value:
        lt_index -= 1

    temp = array[lt_index]
    array[lt_index] = array[start]
    array[start] = temp
    __so_quick(array, start, lt_index-1)
    __so_quick(array, lt_index+1, end)


# 快速排序
@ptime
def so_quick(array):
    _array = copy.deepcopy(array)
    __so_quick(_array, 0, len(_array)-1)
    return _array

if __name__ == '__main__':
    array = [random.randint(0, 3) for i in range(100)]
    # array = [random.randint(0, 20) for i in range(20)]
    print()
    # insert(array)
    insert2(array)
    result = merge_sort(array)
    # result = merge_sort2(array)
    result = so_quick(array)
