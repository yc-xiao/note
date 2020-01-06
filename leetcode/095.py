# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

    def add(self, x):
        if x > self.val:
            if not self.right:
                self.right = TreeNode(x)
            else:
                self.right.add(x)
        else:
            if not self.left:
                self.left = TreeNode(x)
            else:
                self.left.add(x)

def func(array):
    # 列出数组的所有组合
    if len(array) == 2:
        return [array, array[::-1]]
    arrays = []
    for i in range(len(array)):
        new_array = array[:]
        node = new_array.pop(i)
        results = func(new_array)
        for each in results:
            each.append(node)
            arrays.append(each)
    return arrays


def make_tree(array):
    # 将一个数组变成树
    root = TreeNode(array[0])
    for i in range(1, len(array)):
        root.add(array[i])
    return root

def pp(nodes):
    # 用于打印树
    values, _nodes = [], []
    for node in nodes:
        if not node:
            values.append(None)
            continue
        values.append(node.val)
        _nodes.append(node.left)
        _nodes.append(node.right)
    if _nodes:
        values.extend(pp(_nodes))
    return values

class Solution:
    def generateTrees(self, n: int) -> List[TreeNode]:
        if n == 1:
            return [TreeNode(1)]
        size = n

        array = [i for i in range(1, size+1)]
        # 获取所有可能性
        arrays = func(array)
        trees = []

        results = set()
        for array in arrays:
            # 构成树
            tree = make_tree(array)
            # 获取打印结果
            result = pp([tree])
            result = tuple(result)
            # 去重
            if result not in results:
                results.add(result)
                trees.append(tree)
        return trees
"""
    假设: [1,2,3]
    第一步:获取数组所有排列，有六种[1,2,3], [1,3,2,], [2,1,3], [2,3,1], [3,1,2], [3,2,1] 通过func函数实现
    第二步:将数组变成树，通过make_tree实现
    第三步:因为六种可以构成的树存在重复，通过打印结果pp判断哪些重复(去重)
"""
