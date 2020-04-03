import threading
import pymongo
import pdb

client = pymongo.MongoClient(connect=False)

test_db = client.test

lock = threading.Lock()

num = 10
name = 'test'

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
    condition = {'name': name}
    data = test_db.log.find_one(condition)
    for i in range(num):
        if not data['json'][i]:
            data['json'][i] = True
            break
    test_db.log.update_one(condition, {'$set': {'json':data['json']}})

def test_thread():
    ths = []
    for i in range(num):
        th = threading.Thread(target=func)
        th.start()
        ths.append(th)
    for th in ths:
        th.join()

def test_print():
    from pprint import pprint
    condition = {'name': name}
    datas = test_db.log.find(condition)
    for data in datas:
        pprint(data)

def main():
    init_data()
    test_thread()
    test_print()

if __name__ == '__main__':
    main()
