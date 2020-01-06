import random

array = random.sample([i for i in range(1000)], 18)
# array = random.sample([i for i in range(10000)], 10000)
print(array)
print()

# 0,1
def merage(array):
    count = len(array)
    i = 0
    mid = int(count//2)
    j = mid + 1
    _array = []
    while i <= mid or j < count:
        if i > mid:
            _array.append(array[j])
            j+=1
        elif j > count:
            _array.append(array[i])
            i+=1
        elif array[i] < array[j]:
            _array.append(array[i])
            i+=1
        else:
            _array.append(array[j])
            j+=1
    print(_array)
    return _array


def func(array):
    count = len(array)
    num = 2
    while num/2 <= count:
        group_num = int(count/num + 0.5)
        for i in range(0, count, num):
            array[i:i+num] = merage(array)
        num *= 2


if __name__ == '__main__':
    func(array)
