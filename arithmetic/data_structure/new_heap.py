class Node(object):
    def __init__(self, value=None, pp=None, sl=None, sr=None):
        self.value = value
        self.pp = pp
        self.sl = sl
        self.sr = sr

    def add(self, node):
        if self.sl and self.sr:
            print("???")
        if self.sl:
            self.sr = node
        else:
            self.sl = node
        node.pp = self

    def up_patch(self):
        if not self.pp:
            return
        if self.pp.value <= self.value:
            return
        self.change_node(self.pp, self)
        self.up_patch()

    def get_son_node(self):
        if self.sl and self.sr:
            if self.sl.value < self.sr.value:
                return self.sl
            return self.sr
        return self.sl

    def down_patch(self):
        snode = self.get_son_node()
        if not snode:
            return
        if snode.value < self.value:
            self.change_node(self, snode)
            self.down_patch()

    def change_node(self, pnode, snode):
        # 两个节点交换,还要注意指针
        if pnode.pp:
            if pnode.pp.sl == pnode:
                pnode.pp.sl = snode
            elif pnode.pp.sr == pnode:
                pnode.pp.sr = snode
            else:
                print('这里有错误!')
        snode.pp = pnode.pp

        slnode, srnode = snode.sl, snode.sr
        if pnode.sl == snode:
            snode.sr = pnode.sr
            if pnode.sr:
                pnode.sr.pp = snode

            snode.sl = pnode
        elif pnode.sr == snode:
            snode.sl = pnode.sl
            if pnode.sr:
                pnode.sl.pp = snode
            snode.sr = pnode
        else:
            print('这里也有错误!')
        pnode.pp = snode

        pnode.sl = slnode
        pnode.sr = srnode

        if pnode.sl:
            pnode.sl.pp = pnode
        if pnode.sr:
            pnode.sr.pp = pnode

    def __repr__(self):
        return f'{self.value} {self.sl} {self.sr}'


class Heap(object):
    def __init__(self):
        self.root = None

    def add(self, value):
        node = Node(value)
        if not self.root:
            self.root = node
            return node
        pnode = self.search()
        pnode.add(node)
        node.up_patch()
        if not node.pp:
            self.root = node

    def get(self):
        if not self.root:
            return
        node = self.root
        end_node = self.search_end()
        if end_node.pp and end_node.pp.sl == end_node:
            end_node.pp.sl = None
        if end_node.pp and end_node.pp.sr == end_node:
            end_node.pp.sr = None
        end_node.pp = None
        end_node.sl = node.sl
        end_node.sr = node.sr

        if node.sr:
            node.sr.pp = end_node
        if node.sl:
            node.sl.pp = end_node
        self.root = end_node
        snode = node.get_son_node()
        if snode:
            self.root = snode
            end_node.down_patch()
        return node.value

    def search_end(self):
        if not self.root:
            return
        nodes = [self.root]
        while nodes:
            temp_nodes = []
            for node in nodes:
                if node.sl:
                    temp_nodes.append(node.sl)
                if node.sr:
                    temp_nodes.append(node.sr)
            if not temp_nodes:
                return nodes[-1]
            nodes = temp_nodes

    def search(self):
        if not self.root:
            return
        nodes = [self.root]
        while nodes:
            temp_nodes = []
            for node in nodes:
                if not node.sr or not node.sl:
                    return node
                temp_nodes.append(node.sl)
                temp_nodes.append(node.sr)
            nodes = temp_nodes


if __name__ == '__main__':
    heap = Heap()
    # 该堆最后两个值有bug
    nums = [i for i in range(100,-1,-1)]
    print(nums)
    [heap.add(i) for i in nums]
    for i in nums:
        print(heap.get())


    for i in range(len(array)-1):
        for j in range(len(array) - i - 1):
            if array[j] > array[j+1]:
                temp = array[j]
                array[j] = array[j+1]
                array[j+1] = temp
    print(array)
