# 宽度优先
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

def span(nodes):
    if not nodes:
        return
    temp_nodes = []
    for node in nodes:
        print(node.value, end='  ')
        if node.sl:
            temp_nodes.append(node.sl)
        if node.sr:
            temp_nodes.append(node.sr)
    print()
    span(temp_nodes)


if __name__ == '__main__':
    node = Node(10)
    func(node, 10, deep=10)
    span([node])
