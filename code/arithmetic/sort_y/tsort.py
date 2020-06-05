import random
import time

num = 10
array = random.sample([i for i in range(num*10)], num)
"""
def sort(array, l, r):
    # 如果两个指针相遇则退出，闭区间
    if l >= r:
        return

    # 随机取一个值，开始两边跑
    i,j = l,r
    num = array[i]

    while i<j:
        while i<j and array[i]<=num:
            i+=1
        while i<j and array[j]>num:
            j-=1
        if i<j:
            array[i], array[j] = array[j], array[i]
            i+=1
            j-=1
    if array[i] > num:
        i-=1

    array[i], array[l] = array[l], array[i]
    sort(array, l, i-1)
    sort(array, i+1, r)

sort(array, 0, len(array)-1)

class MinHeap(object):
    '''
        堆就是一个二叉树，并且父节点要大于/小于两个子节点
    '''
    def __init__(self):
        # 维护一个数组
        # 最小值放在 0
        self.array = []
        self.ll = -1

    def get(self):
        if self.ll == -1:
            return
        elif self.ll == 0:
            return self.array.pop()

        num = self.array[0]
        self.array[0] = self.array.pop()
        self.ll-=1
        self.down(0)
        return num

    def add(self, num):
        self.array.append(num)
        self.ll+=1
        self.up(self.ll)

    def up(self, index):
        if index == 0:
            return
        pindex = (index-1)//2
        if self.array[pindex] > self.array[index]:
            self.array[pindex], self.array[index] = self.array[index], self.array[pindex]
            self.up(pindex)

    def down(self, index):
        lson, rson = index*2+1, index*2+2

        if lson > self.ll:
            return
        elif rson > self.ll:
            son = lson
        elif self.array[lson] < self.array[rson]:
            son = lson
        elif self.array[lson] > self.array[rson]:
            son = rson
        else:
            return
        if self.array[index] > self.array[son]:
            self.array[index], self.array[son] = self.array[son], self.array[index]
            self.down(son)

def sort(array):
    # 堆排序
    min = MinHeap()
    for i in array:
        min.add(i)
    print([min.get() for i in array])

def sort(array):
    # 归并排序，采用递归的排序方式
    # 将数组一分为2，并假设子数组已排序好
    # 处理子数组排序， 问题变成 a = [1,4,6] b =[2,9] 合并排序
    ll = len(array)
    if ll < 2:
        return array
    if ll == 2:
        return array if array[0] < array[1] else array[::-1]

    half = ll//2
    left_array = sort(array[:half])
    right_array = sort(array[half:])

    # 上面已经排序完了
    new_array = []
    i, j = 0, 0
    ll, rl = len(left_array), len(right_array)
    for k in range(ll+rl):
        if i == ll:
            new_array.append(right_array[j])
            j+=1

        elif j == rl:
            new_array.append(left_array[i])
            i+=1

        elif left_array[i] < right_array[j]:
            new_array.append(left_array[i])
            i+=1

        else:
            new_array.append(right_array[j])
            j+=1
    return new_array

def sort(array):
    # 插入排序
    # 从小到大排序，从i+1个位置向前排列
    # O(n2)-> O(n) 希尔排序， 插入排序很关键
    ll = len(array)
    for i in range(1, ll):
        while i > 0 and array[i-1] > array[i]:
            array[i-1], array[i] = array[i], array[i-1]
            i-=1

    print(array)

def sort(array):
    # 选择排序
    # 找出最大，放到尾部
    # O(n2)
    ll = len(array)
    for j in range(ll-1):
        for i in range(ll-1-j):
            if array[ll-1-j] < array[i]:
                array[ll-1-j], array[i] =  array[i], array[ll-1-j]
    print(array)

def sort(array):
    # 时间复杂度是O(n2)
    # 从第一个数跟第二个数比较，交换位置
    # 总共需要排列n-1次
    ll = len(array)
    for j in range(ll-1):
        for i in range(ll-1-j):
            if array[i] < array[i+1]:
                array[i], array[i+1] = array[i+1], array[i]
    print(array)
"""
