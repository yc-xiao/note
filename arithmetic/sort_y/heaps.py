"""
    堆排序:队列优先
    索引堆
    大小堆类
"""

import operator
import random

class MinHeap:
    def __init__(self):
        self.array = ['helloc',]
        self.count = 0

    def getMax(self):
        if not self.count:
            print('堆为空')
            return
        self.array[1], self.array[-1] = self.array[-1], self.array[1]
        max = self.array.pop()
        self.count-=1
        if self.count:
            self.down(1)
        return max

    def add(self, value):
        self.array.append(value)
        self.count += 1
        self.up(self.count)

    def up(self, size):
        # 将节点向上移动
        parent_size = size // 2
        if size > 1 and self.array[size] < self.array[parent_size]:
            self.array[size], self.array[parent_size] = self.array[parent_size], self.array[size]
            self.up(parent_size)

    def down(self, size):
        # 将节点向下移动
        left, right = size*2, size*2+1
        if left > self.count:
            return
        elif right > self.count:
            if self.array[size] > self.array[left]:
                self.array[size], self.array[left] = self.array[left], self.array[size]
        else:
            if self.array[left] <= self.array[right] and self.array[left] < self.array[size]:
                self.array[size], self.array[left] = self.array[left], self.array[size]
                self.down(left)
            elif self.array[right] <= self.array[left] and self.array[right] < self.array[size]:
                self.array[size], self.array[right] = self.array[right], self.array[size]
                self.down(right)

def test_maxHeap(array):
    heap = MinHeap()
    for i in array:
        heap.add(i)
    print([heap.getMax() for i in range(heap.count)])


class IndexHeap:
    def __init__(self, flag=False):
        # 默认是最小堆
        self.index = 0
        self.datas = [] # 数据存储，可以改变顺序
        self.indexs = [] # 堆排序存储，可以改变顺序，数据之间的排序通过indexs去排序
        self.logs = [] # 用于记录原先数据的位置，例如原先datas=[1,2,3]，由于数据交换改为datas=[3,2,1]。通过logs可以查找到1


    def add(self, value):
        self.datas.append(value)
        self.indexs.append(self.index)
        self.logs.append(self.index)
        self.index+=1
        self.up(self.index-1)

    def _get(self, index):
        return self.datas[self.indexs[index]]

    def get_by_log(self, index):
        # 最初存的位置
        pos = self.logs[index]
        if pos > self.index-1:
            return None
        return self.datas[pos]

    def get(self):
        if not self.index:
            print('当前堆为空')

        # 堆顶跟堆底交换
        self.indexs[0], self.indexs[-1] = self.indexs[-1], self.indexs[0]
        pos = self.indexs[-1] # 获取到datas最大值所在位置
        # 取出datas的最大值
        self.datas[pos], self.datas[-1] = self.datas[-1], self.datas[pos]
        self.logs[pos], self.logs[-1] = self.index, pos

        pos = self.indexs.pop()
        data = self.datas.pop()
        self.index-=1

        # 将indexs内指向datas最后一个的值改为pos
        for i in range(self.index):
            if self.indexs[i] == self.index:
                self.indexs[i] = pos

        self.down(0)
        return data

    def up(self, pos):
        if pos <= 0:
            return
        ppos = (pos-1)//2
        # 最小堆，当前节点是否大于子节点
        if self._get(pos) < self._get(ppos):
            self.indexs[pos], self.indexs[ppos] = self.indexs[ppos], self.indexs[pos]
            self.up(ppos)

    def down(self, pos):
        lpos = pos*2+1
        rpos = pos*2+2
        if lpos > self.index-1:
            return
        if rpos > self.index-1:
            # 说明只有左子节点
            if self._get(pos) > self._get(lpos):
                self.indexs[pos], self.indexs[lpos] = self.indexs[lpos], self.indexs[pos]
        else:
            # 说明有两个子节点
            if self._get(lpos) <= self._get(rpos) and self._get(lpos) < self._get(pos):
                self.indexs[pos], self.indexs[lpos] = self.indexs[lpos], self.indexs[pos]
                self.down(lpos)
            if self._get(rpos) <= self._get(lpos) and self._get(rpos) < self._get(pos):
                self.indexs[pos], self.indexs[rpos] = self.indexs[rpos], self.indexs[pos]
                self.down(rpos)


def test_indexHeap(array):
    indexHeap = IndexHeap()
    for i in array:
        indexHeap.add(i)
    _results = []
    for i in range(indexHeap.index):
        result = indexHeap._get(i)
        _results.append(result)
    print('array:', array)
    print('trees', _results)
    print('indexs', indexHeap.indexs)
    print('index', indexHeap.index)

    results = []
    for i in range(10):
        result = indexHeap.get()
        results.append(result)
    log_results = []
    for i in range(100):
        log_results.append(indexHeap.get_by_log(i))
    print(results)
    print(log_results)


if __name__ == '__main__':
    array = [random.randint(1, 10005) for i in range(100)]
    # array = [i for i in range(1000)]
    # test_maxHeap(array)
    test_indexHeap(array)
