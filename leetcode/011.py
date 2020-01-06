"""
    1.找到数组的两两组合,并计算面积，求面积的最大值
"""

def func(p1, p2):
    length = p2[0] - p1[0]
    height = p1[1] if p1[1] < p2[1] else p2[1]
    return length * height

if __name__ == '__main__':
    array = [1,8,6,2,5,4,8,3,7]
    nums = len(array)
    results = []
    array = [1,8,6,2,5,4,8,3,7]
    nums = len(array)
    results = []
    for i in range(nums):
        for j in range(nums-1, i, -1):
            p1 = (i, array[i])
            p2 = (j, array[j])
            results.append(func(p1, p2))
            if array[j] >= array[i]:
                break
    print(results)
    result = max(results)
    print(result)
