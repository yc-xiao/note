# 二叉树 前中后遍历
# 完全二叉树不等于满二叉树， 满二叉树一定是完全二叉树

# https://www.jianshu.com/p/456af5480cee
# 先序：1 2 4 6 7 8 3 5
# 中序：4 7 6 8 2 1 3 5
# 后序：7 8 6 4 2 5 3 1

class Node(object):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def pre(node):
    # 根左右
    if not node:
        return
    print(node.value, end=' ')
    pre(node.left)
    pre(node.right)

def mid(node):
    # 左根右
    if not node:
        return
    mid(node.left)
    print(node.value, end=' ')
    mid(node.right)

def last(node):
    # 左右跟
    if not node:
        return
    last(node.left)
    last(node.right)
    print(node.value, end=' ')

def test():
    node6 = Node(6, Node(7), Node(8))
    node4 = Node(4, None, node6)
    node2 = Node(2, node4)
    node3 = Node(3, None, Node(5))
    node1 = Node(1, node2, node3)
    pre(node1)
    print()
    mid(node1)
    print()
    last(node1)
    print()

test()
