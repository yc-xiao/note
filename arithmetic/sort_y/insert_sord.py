# 插入排序 O(n2)
import random

temp_array = []
array = random.sample([i for i in range(10000)], 10)
array = random.sample([i for i in range(100000)], 10000)
print(array)

def insert_temps(array):
    temp_array.append(array[0])
    for i in range(1, len(array)):
        for j in range(0, len(temp_array)):
            if array[i] < temp_array[j]:
                temp_array.insert(j, array[i])
                break
        else:
            temp_array.append(array[i])
    print(temp_array)

def insert(array):
    count = len(array)
    for i in range(1, count):
        value = array[i]
        while i > 0 and array[i-1] > value:
            array[i] = array[i-1]
            i-=1
        array[i] = value
    print(array)

# 对区间[s,e] 进行快速排序
def _insert(array, start, end):
    # 1.遍历[s+1, e]区间
    for i in range(start+1, end+1):
        # 2.取i，与已排好序的区间做对比，移动数组
        value = array[i]
        while i > start and array[i-1] > value:
            array[i] = array[i-1]
            i-=1
        array[i] = value

if __name__ == '__main__':
    # insert_temps(array)
    # insert(array)
    _insert(array, 0, len(array)-1)
    print(array)
