# 时间复杂度O(n2)
import random

array = random.sample([i for i in range(10000)], 10000)
print(array)


for i in range(len(array)-1):
    for j in range(len(array) - i - 1):
        if array[j] > array[j+1]:
            temp = array[j]
            array[j] = array[j+1]
            array[j+1] = temp
print(array)
