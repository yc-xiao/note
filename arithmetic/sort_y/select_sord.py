# 选择排序
# 时间复杂度 O(n2)

import random

array = random.sample([i for i in range(10000)], 10000)
print(array)
for i in range(len(array)-1):
    max = 0
    for j in range(len(array)-i):
        if array[max] < array[j]:
            max = j
    temp = array[max]
    array[max] = array[len(array)-i-1]
    array[len(array)-i-1] = temp

print(array)
