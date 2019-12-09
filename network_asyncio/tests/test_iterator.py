
class A(object):
    def __init__(self):
        self.list = [i for i in range(3)]
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.list):
            value = self.list[self.index]
            self.index += 1
            return value
        raise StopIteration("到头了...")
