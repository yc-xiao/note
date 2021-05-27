"""
    迭代: 可进行 for 遍历
        迭代器: 实现__iter__方法，该方法返回可迭代对象。
        可迭代对象: 实现__next__方法，for遍历本职就是调用next方法
        生成器: 实现__next__方法，yield
"""
import pdb

def product():
    print('开始干活')
    return_str = f'启动'
    while True:
        receive_str = yield return_str
        if return_str == 0:
            return '关机'
        return_str = receive_str

pdb.set_trace()
tp = product()
print('')
# print(p.send(None))
# print(p.send('生产第一件'))
# print(p.send('生产第二件'))
# print(p.send('back'))
