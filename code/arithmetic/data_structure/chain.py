'''
    链表是数据结构之一，其中的数据呈线性排列。
    在链表中，数据的添加和删除都较为方便， 就是访问比较耗费时间
    查询时间:O(n)
    添加和删除时间:O(1) PS:需要先找到数据(O(n))
    循环链表:循环链表没有头和尾的概念。想要保存数量固定的最新数据时通常会使用这种链表。
    双向链表: 可以双向遍历，查询更方便，修改麻烦。存储大
'''

# 定义结构体
class Node(object):
    def __init__(self, value, next_id=None):
        self.value = value
        self.next_id = next_id
    def __repr__(self):
        return f'id:{id(self)} ---> value:{self.value} ---> next_id:{self.next_id}'

# 定义链表的数据结构
class Chain(object):
    def __init__(self):
        # 当前指针和头指针
        self.id_object = {}
        self.head = None
        self.current_head = None

    def __repr__(self):
        return f'head:{self.head} current_head:{self.current_head} '

    # 返回最后一个节点
    def get_end_node(self):
        if self.current_head:
            return self.id_object[self.current_head]

    # 返回头节点:
    def get_first_node(self):
        if self.head:
            return self.id_object[self.head]

    # 添加方式在节点后面补充，另一种添加方式在节点前补充(移动头指针)
    def add_node(self, node):
        addr = id(node)
        self.id_object[addr] = node
        if not self.head:
            self.current_head = self.head = addr
            return
        temp_node = self.id_object[self.current_head]
        self.current_head = temp_node.next_id = id(node)
        self.get_all()

    def get_all(self):
        current_head = self.head
        while current_head:
            cur_node = self.id_object[current_head]
            current_head = cur_node.next_id
            print(f'哒哒哒:---> {cur_node}')

    def get_node_by_value(self, value):
        current_head = self.head
        while current_head:
            cur_node = self.id_object[current_head]
            if cur_node.value == value:
                return cur_node
            current_head = cur_node.next_id

    def insert_node(self, node1, node2):
        # 在节点1后面添加节点2
        addr = id(node2)
        self.id_object[addr] = node2
        temp_next_id = node1.next_id
        node1.next_id = id(node2)
        node2.next_id = temp_next_id
        self.get_all()

    def delete_value(self, value):
        p_node = None
        current_head = self.head
        while current_head:
            cur_node = self.id_object[current_head]
            if cur_node.value == value:
                if not p_node:
                    self.head = cur_node.next_id
                    if not self.head:
                        self.current_head = None
                else:
                    p_node.next_id = cur_node.next_id
                    if not p_node.next_id:
                        self.current_head = id(p_node)
            p_node = cur_node
            current_head = cur_node.next_id
        self.get_all()

def main():
    chain = Chain()
    while True:
        value = input('请输入值，按b退出：')
        if value == 'b':
            break
        node = Node(value)
        chain.add_node(node)
    chain.get_all()
    pdb.set_trace()

if __name__ == '__main__':
    main()
