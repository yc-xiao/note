"""
像栈这种最后添加的数据最先被取出，即“后进先出”的结构，我们称为 Last In
First Out，简称 LIFO。
与链表和数组一样，栈的数据也是线性排列，但在栈中，添加和删除数据的操作只
能在一端进行，访问数据也只能访问到顶端的数据。想要访问中间的数据时，就必须通
过出栈操作将目标数据移到栈顶才行。
栈只能在一端操作这一点看起来似乎十分不便，但在只需要访问最新数据时，使用
它就比较方便了。
深度优先搜索算法，通常会选择最新的数据作为候补顶点。在候补顶点的管理上就可以使用栈。
场景:递归，函数保存
时间复杂度 O(1)
"""
from array import Array

class Stack(object):
    def __init__(self, size=10):
        self.array = Array(size)
        self.size = size
        self.index = -1

    def __repr__(self):
        return f'{self.index}, {self.array}'

    def pop(self):
        result = self.get()
        if result:
            self.array.delete(self.index)
            self.index -= 1
        return result

    def push(self, value):
        if self.index + 1 < self.size:
            self.array.add(value)
            self.index += 1

    def get(self):
        if self.index < 0:
            return None
        return self.array.get(self.index)

stack = Stack()

import pdb;pdb.set_trace()
stack
