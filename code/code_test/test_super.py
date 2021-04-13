class A:
    def __init__(self, n):
        self.n = n
        print(f'A -> {self.n}')

class B:
    def __init__(self):
        print(f'B -> {self.n}')


class C(A, B):
    def __init__(self, n):
        print(f'C -> {n}')
        super().__init__(n)  # 等同于下一行，先找A,如果A没有再找B，就近找
        super(C, self).__init__(n)
        A.__init__(self, n)
        B.__init__(self)

c = C(1)
print(c.n)
