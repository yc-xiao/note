# 病龟排序(归并排序)
# 时间复杂度为O(nlogn)
# from queue import Queue
import random

array = random.sample([i for i in range(1000)], 10)
array = random.sample([i for i in range(10000)], 10000)
print(array)

def split(array):
    count = len(array)
    if count < 2:
        return array

    first_array, end_array = [],[]
    half = count//2
    for i in range(half):
        first_array.append(array[i])
    first_array = split(first_array)
    for i in range(half, count):
        end_array.append(array[i])
    end_array = split(end_array)

    # 数组交换时间可能比较长，可以选择链表替代
    new_array = []
    while len(first_array):
        if len(end_array) == 0:
            break
        first_value = first_array[0]
        end_value = end_array[0]
        if first_value < end_value:
            new_array.append(first_value)
            first_array = first_array[1:]
        else:
            new_array.append(end_value)
            end_array = end_array[1:]
    if len(first_array) == 0:
        new_array.extend(end_array)
    if len(end_array) == 0:
        new_array.extend(first_array)
    return new_array

def main(array):
    array = split(array)
    print(array)

if __name__ == '__main__':
    main(array)
