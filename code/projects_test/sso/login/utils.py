from random import randint
from flask import session
import requests

# ts缓存
redis_cache = {}

# 记录用户在apps建立的会话，注销时使用
apps_cache = {}

def is_login():
    # 登录验证装饰器
    print('session -> ', session)
    if 'username' in session:
        return True
    else:
        return False

def set_ts(username, return_url):
    if not redis_cache.get(username):
        redis_cache[username] = randint(1000, 9999)
    urls = apps_cache.get(username, set())
    urls.add(return_url)
    return redis_cache[username]

def get_ts(username):
    return str(redis_cache[username])

def clear_ts(username):
    redis_cache.pop(username, None)
    logout(username)

def logout(username):
    # url -> url+token
    urls = apps_cache.get(username, [])
    for url in urls:
        res = requests.get(url)
        if res.status_code != 200:
            print(f'{url}, logout err')
