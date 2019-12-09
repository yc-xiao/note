from pprint import pprint
'''
    修改版链表:
        用一个空的头节点保存头指针，保持数据结构一致(全部是节点)
'''
class Node(object):
    def __init__(self, value=None):
        self.value = value
        self.next = None
    def __repr__(self):
        return f'{self.value}, {self.next}'

class Chain(object):
    def __init__(self):
        self.MAP = {
            # "id": Node
        }
        node = Node()
        self.head = id(node)
        self.current_head = None
        self.MAP[self.head] = node

    def __repr__(self):
        pprint(self.MAP)
        print(self.head)
        print(self.current_head)
        return 'end'

    def add(self, value):
        node = Node(value)
        if self.current_head:
            cur_node = self.MAP[self.current_head]
            cur_node.next = id(node)
            self.MAP[cur_node.next] = node
            self.current_head = cur_node.next
        else:
            head_node = self.MAP[self.head]
            head_node.next = id(node)
            self.current_head = head_node.next
            self.MAP[self.current_head] = node

    def get_first(self):
        return self.MAP.get(self.MAP[self.head].next, None)

    def get_end(self):
        return self.MAP.get(self.current_head, None)

    def get_all(self):
        head_node = self.MAP[self.head]
        cur_node = head_node
        while cur_node.next:
            cur_node = self.MAP[cur_node.next]
            print(cur_node)

    def delete(self, value):
        head_node = self.MAP[self.head]
        cur_node = head_node
        while cur_node.next:
            next_node = self.MAP[cur_node.next]
            if value == next_node.value:
                self.MAP.pop(cur_node.next)
                cur_node.next = next_node.next
                if not next_node.next:
                    self.current_head = id(cur_node)
                break
            cur_node = next_node

    def insert(self, value, node):
        new_node = Node(value)
        new_node.next = node.next
        node.next = id(new_node)
        self.MAP[node.next] = new_node

    def get_node_by_value(self, value):
        head_node = self.MAP[self.head]
        cur_node = head_node
        while cur_node.next:
            cur_node = self.MAP[cur_node.next]
            if value == cur_node.value:
                return cur_node
