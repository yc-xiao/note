# 深度优先算法

class Node(object):
    def __init__(self, value=None, sl=None, sr=None):
        self.value = value
        self.sl = sl
        self.sr = sr

    def add(self, value):
        node = Node(value)
        if not self.sl:
            self.sl = node
        else:
            self.sr = node
        return node

def func(node, value, deep):
    if not deep:
        return
    deep -= 1
    func(node.add(value), value+1, deep)
    func(node.add(value), value+1, deep)

def deep(node):
    # 深度优先
    print(node.value, end=' ')
    if node.sl:
        deep(node.sl)
    print()
    if node.sr:
        deep(node.sr)


if __name__ == '__main__':
    node = Node(10)
    func(node, 10, deep=10)
    deep(node)
