from flask import Flask, request, session, redirect
import requests

app = Flask(__name__)
app.secret_key = b'23333'
login_url = 'http://127.0.0.1:9999'

ts_cache = {}

def to_redirect():
    print(request.full_path, request.url_root)
    return redirect(f'{login_url}/login/?return_path={request.full_path}&return_url={request.url_root}')

@app.route('/')
def index():
    # 未登录则跳转到登录服务
    if 'username' in session:
        return 'nice'
    else:
        return to_redirect()

@app.route('/login/')
def login():
    # 登录服务验证，并记录信息
    ts = request.args.get('ts', None)
    username = request.args.get('username', None)
    return_path = request.args.get('return_path', '/')
    if get_ts:
        res = requests.get(f'{login_url}/check_ts?ts={ts}&username={username}')
        if res.status_code == 200:
            data = res.json()
            print('data -> ', data)
            session['username'] = data.get('username')
            ts_cache[username] = ts
        return to_redirect(return_path)
    else:
        return to_redirect('/')

@app.route('/logout/')
def logout():
    # 注销子会话，通知登录服务注销所有子会话
    username = session.pop('username', None)
    ts = ts_cache.pop(username, None)
    requests.get(f'{login_url}/logout?ts={ts}')
    return 'logout'

if __name__ == "__main__":
    app.run(port=9001)
