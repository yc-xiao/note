"""
# 存在一个bug，233333

堆是一种图的树形结构，被用于实现“优先队列”（priority queue),可以多次取最大或最小值O(1)。
将一堆数据放入一个二叉树下，并排列，根节点是最大或最小值。
频繁地从管理的数据中取出最小值，那么使用堆来操作会非常方便

子结点必定大于父结点。因此，最小值被存储在顶端的根结点中。往堆中添加数据时，为了遵守这条规则，一般会
把新数据放在最下面一行靠左的位置。当最下面一行里没有多余空间时，就再往下另起一行，把数据加在这一行的最左端。

性质:
    1.顶点总是最大或最小值，适用于频繁取最大、小值(优先队列)
    2.父节点总是比子节点大/小，根据这一个性质进行父子节点互换
插入时间复杂度: 对比次数与树的高度有关
取出后时间复杂度: 对比次数与树的深度有关
O(logn)。
"""
class Node(object):
    def __init__(self, value, pp=None, pls=None, prs=None):
        '''
            pp  父节点 pls 左节点 prs 右节点
        '''
        self.value = value
        self.pp = pp
        self.pls = pls
        self.prs = prs

class Heap(object):
    def __init__(self):
        self.root = None

    def show(self):
        nodes = [self.root]
        show_results = []
        while nodes:
            temp_nodes = []
            temp_value = []
            for node in nodes:
                if not node:
                    continue
                temp_value.append(str(node.value))
                if node.pls:
                    temp_nodes.append(node.pls)
                if node.prs:
                    temp_nodes.append(node.prs)
            nodes = temp_nodes
            show_results.append(temp_value)
        nums = len(2**(len(show_results)-1)*'\t')
        for show_result in show_results[:-1]:
            num = int(nums/(len(show_result) + 1))
            tt = '\t'
            print(tt.join(show_result))
        print('\t'.join(show_results[-1]))

    def search_position(self, nodes):
        if not nodes:
            return
        temp_nodes = []
        for node in nodes:
            if not node.pls or not node.prs:
                return node
            temp_nodes.append(node.pls)
            temp_nodes.append(node.prs)
        return self.search_position(temp_nodes)

    def get_root(self):
        return self.root

    def add_value(self, value):
        return self.add_node(Node(value))

    def add_node(self, node):
        if not self.root:
            self.root = node
            return
        cur_node = self.search_position([self.root])
        direction = self.is_l_or_r(cur_node)
        setattr(cur_node, direction, node)
        node.pp = cur_node
        self.adjust(node)

    def get_end_node(self, nodes=[]):
        temp_nodes = []
        for node in nodes:
            if node.pls:
                temp_nodes.append(node.pls)
            if node.prs:
                temp_nodes.append(node.prs)
        if not temp_nodes:
            return nodes[-1]
        return self.get_end_node(temp_nodes)

    def get_value(self):
        if not self.root:
            return

        end_node = self.get_end_node([self.root])
        direction = self.is_l_or_r(end_node.pp, end_node)
        setattr(end_node.pp, direction, None)

        root_node = self.root

        end_node.pp = None
        end_node.pls = self.root.pls
        end_node.prs = self.root.prs
        if self.root.pls:
            self.root.pls = end_node
        if self.root.pls:
            self.root.pls = end_node
        self.root = end_node
        flag = True

        while end_node:
            temp_node = self.get_min(end_node)
            if temp_node and temp_node.value < end_node.value:
                self.exchange_position(end_node, temp_node)
                if flag:
                    flag = False
                    self.root = temp_node
            else:
                break
        return root_node

    def get_min(self, node):
        if not node.prs and not node.pls:
            return
        if node.prs and node.prs.value < node.pls.value:
            return node.prs
        return node.pls


    def is_l_or_r(self, pnode, snode=None):
        # 检测父节点有那个可用
        if not snode:
            return 'prs' if pnode.pls else 'pls'
        # 检测子节点属于父节点的那个子节点
        if pnode.prs and pnode.prs == snode:
            return 'prs'
        elif pnode.pls and pnode.pls == snode:
            return 'pls'
        raise Exception('GG')

    def adjust(self, son_node):
        # 调整堆，特点是子节点比父节点大、小，节点只需要跟父节点比较。
        # 如果错误，则父子节点换位，在向上级比较。
        if not son_node.pp:
            self.root = son_node
            return

        if son_node.value < son_node.pp.value:
            self.exchange_position(son_node.pp, son_node)
            self.adjust(son_node)

    def exchange_position(self, pnode, son_node):
        # 修改祖父节点子节点指向
        if pnode.pp:
            direction = self.is_l_or_r(pnode.pp, pnode)
            setattr(pnode.pp, direction, son_node)
        direction = self.is_l_or_r(pnode, son_node)
        # 交换两个节点位置
        son_node.pp = pnode.pp
        temp_son_node_pls = son_node.pls
        temp_son_node_prs = son_node.prs
        if direction == 'pls':
            son_node.pls = pnode
            son_node.prs = pnode.prs
            pnode.pp = son_node
            if pnode.prs:
                pnode.prs.pp = son_node
        else:
            son_node.pls = pnode.pls
            son_node.prs = pnode
            pnode.pp = son_node
            if pnode.pls:
                pnode.pls.pp = son_node
        pnode.pls = temp_son_node_pls
        pnode.prs = temp_son_node_prs
        if temp_son_node_pls:
            temp_son_node_pls.pp = pnode
        if temp_son_node_prs:
            temp_son_node_prs.pp = pnode

if __name__ == "__main__":
    heap = Heap()
    [heap.add_value(i) for i in range(100, 95, -1)]
    heap.show()
    print([heap.get_value().value for i in range(100, 97, -1)])
    import pdb;pdb.set_trace()
    heap.show()
    heap.get_value()
    heap.show()
