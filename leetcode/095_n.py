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
    root = TreeNode(array[0])
    for i in range(1, len(array)):
        root.add(array[i])
    return root

def pp(nodes):
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

if __name__ == '__main__':
    size = 3
    array = [i for i in range(1, size+1)]
    arrays = func(array)
    trees = []
    results = set()
    for array in arrays:
        tree = make_tree(array)
        result = pp([tree])
        result = tuple(result)
        if result not in results:
            results.add(result)
            trees.append(tree)
    return trees
