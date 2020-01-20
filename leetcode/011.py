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
    start, end = 0, nums-1
    results = []
    for i in range(nums):
        # 比较头尾，选择最小值做定点
        # 从定点的另一侧往回比较，找去区间最大值
        if array[start] > array[end]:
            # 取小的 array[end]
            for j in range(start, end):
                p1 = (j, array[j])
                p2 = (end, array[end])
                results.append(func(p1, p2))
                if array[j] >= array[end]:
                    break
            end-=1
        else:
            # 取小的 array[i]
            for j in range(end, start, -1):
                p1 = (start, array[start])
                p2 = (j, array[j])
                results.append(func(p1, p2))
                if array[j] >= array[start]:
                    break
            start+=1

    print(results)
    result = max(results)
    print(result)
