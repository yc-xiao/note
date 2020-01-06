# 插入排序 O(n2)
import random

temp_array = []
array = random.sample([i for i in range(10000)], 10)
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

if __name__ == '__main__':
    insert_temps(array)
    insert(array)
