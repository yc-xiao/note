class AbsInt:
    def __new__(cls, *args, **kw):
        print(args, kw)
        cls.n = abs(args[0])
        return super().__new__(cls)

class A(AbsInt):
    def __init__(self, n):
        pass

a = A(-1)
print(a, a.n)
