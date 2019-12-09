# 快排 O(n)
# 这个有点不太对　２３３３３
import random

array = random.sample([i for i in range(10000)], 10000)

def so_sort(array, left, right):
    if right <= left:
        return
    index = random.sample(range(left, right+1), 1)[0]
    base_num = array[index]

    left_array,right_array, mi_array = [], [], []
    for i in range(left, right+1):
        if array[i] > base_num:
            right_array.append(array[i])
        elif array[i] < base_num:
            left_array.append(array[i])
        else:
            mi_array.append(array[i])

    array[left: right+1] = left_array + mi_array + right_array
    so_sort(array, left=left, right=len(left_array)-1)
    so_sort(array, left=len(left_array) + len(mi_array), right=right)

def main():
    print(array)
    so_sort(array, 0, len(array)-1)
    print(array)

if __name__ == "__main__":
    main()
