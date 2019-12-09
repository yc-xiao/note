"""
像队列这种最先进去的数据最先被取来，即“先进先出”的结构，我们称为 First In
    First Out，简称 FIFO。
与栈类似，队列中可以操作数据的位置也有一定的限制。在栈中，数据的添加和删
除都在同一端进行，而在队列中则分别是在两端进行的。队列也不能直接访问位于中间
的数据，必须通过出队操作将目标数据变成首位后才能访问。
"""
from chain import Chain, Node

class Queue(object):
    def __init__(self):
        self.chain = Chain()

    def __repr__(self):
        self.chain.get_all()
        return f'{self.chain}'

    def add(self, value):
        self.chain.add_node(Node(value))

    def out(self):
        node = self.chain.get_first_node()
        if node:
            self.chain.delete_value(node.value)
        print(node)

queue = Queue()
