import multiprocessing
import pymongo
import pdb

client = pymongo.MongoClient()
num, name = 10, 'test'

test_db = client.test
lock = multiprocessing.Lock()

def add_lock(func):
    def inner(*args, **kw):
        with lock:
            result = func(*args, **kw)
        return result
    return inner

def init_data():
    test_data = {
        'name': name,
        'json': [False for i in range(num)]
    }
    condition = {'name': name}
    data = test_db.log.delete_one(condition)
    test_db.log.insert_one(test_data)

@add_lock
def func():
    # 数据库找到 name
    client = pymongo.MongoClient()
    test_db = client.test
    lock = multiprocessing.Lock()
    condition = {'name': name}
    data = test_db.log.find_one(condition)
    for i in range(num):
        if not data['json'][i]:
            data['json'][i] = True
            break
    test_db.log.update_one(condition, {'$set': {'json':data['json']}})

def test_process():
    pss = []
    for i in range(num):
        ps = multiprocessing.Process(target=func)
        ps.start()
        pss.append(ps)

    for ps in pss:
        ps.join()

def test_print():
    from pprint import pprint
    condition = {'name': name}
    datas = test_db.log.find(condition)
    for data in datas:
        pprint(data)

def main():
    init_data()
    test_process()
    test_print()

if __name__ == '__main__':
    main()
