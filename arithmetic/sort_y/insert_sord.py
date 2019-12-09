# 插入排序 O(n2)
import random

temp_array = []
array = random.sample([i for i in range(10000)], 10000)
print(array)
temp_array.append(array[0])
for i in range(1, len(array)):
    for j in range(0, len(temp_array)):
        if array[i] < temp_array[j]:
            temp_array.insert(j, array[i])
            break
    else:
        temp_array.append(array[i])
print(temp_array)
