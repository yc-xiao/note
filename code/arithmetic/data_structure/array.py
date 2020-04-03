"""
在链表和数组中，数据都是线性地排成一列。
    在链表中访问数据较为复杂，添加和删除数据较为简单；
    而在数组中访问数据比较简单，添加和删除数据却比较复杂。
"""
class Array(object):
    def __init__(self, size=10):
        self.count = 0
        self.size = size
        self.array = [None for i in range(self.size)]

    def __repr__(self):
        return f'count: {self.count} size:{self.size} array:{self.array}'

    def get(self, index=0):
        if index > self.count or index < 0:
            return '索引错误'
        return self.array[index]

    def get_all(self):
        print(self.array)

    def delete(self, index):
        if index > self.count or index < 0:
            return '索引错误'
        for i in range(index, self.count-1):
            self.array[i] = self.array[i+1]
        self.array[self.count-1] = None
        self.count -= 1

    def add(self, value):
        self.count += 1
        if self.count > self.size:
            self.count -= 1
            return '数组已满'
        self.array[self.count-1] = value

    def insert(self, value, index=0):
        self.count += 1
        if self.count > self.size:
            self.count -= 1
            return '数组已满'
        if index > self.size or index < 0:
            return '索引错误'
        for i in range(self.size-index):
            self.array[self.size-i-1] = self.array[self.size-i-2]
        self.array[index] = value

array = Array()
