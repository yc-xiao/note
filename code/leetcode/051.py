# N皇后问题
from pprint import pprint

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return self.__str__()


def ok(p1, p2):
    if p1.x == p2.x:
        return False
    elif p1.y == p2.y:
        return False
    elif p1.x - p2.x == p1.y - p2.y:
        return False
    elif p1.x - p2.x == -1 * (p1.y-p2.y):
        return False
    else:
        return True

def newpoints(p, ps):
    return [_ for _ in ps if ok(p, _)]

def calN(ps, n):
    if n == 1:
        return [ps] if ps else []
    n-=1
    results = []
    for p in ps:
        nps = newpoints(p, ps)
        if not nps:
            return []
        result = calN(nps, n)
        for each in result:
            if each:
                each.append(p)
        results.extend(result)
    return results

def change(results, n):
    nresults = []
    for each in results:
        tset = set()
        for p in each:
            tset.add((p.x, p.y))
        ss = []
        for i in range(n):
            s = ''
            for j in range(n):
                if (i,j) in tset:
                    s+='Q'
                else:
                    s+='.'
            ss.append(s)
        nresults.append(ss)
    return nresults

if __name__ == '__main__':
    n = 8 # 1
    points = [Point(i, j) for i in range(n) for j in range(n)]
    print(points)
    results = calN(points, n)

    nresults = []
    for each in results:
        if set(each) not in nresults:
             nresults.append(set(each))
    n = change(nresults, n)
    pprint(n)
    # 一个可放位置的集合，取一个点，递归Ｎ次
    # 再找第二个可能落下的点
    # 在找第三个可能落下的点
    # 超时。根据对称性应该可以减半优化
