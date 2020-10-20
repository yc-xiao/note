'''
    1.登录接口
    2.测试接口
    3.注销接口
'''
from flask import Flask, request, session, redirect, jsonify
from utils import is_login, set_ts, clear_ts, get_ts

# 测试用户
test_users = {
    'xm': {'pwd': '123456', 'nickname': '小明'}
}

app = Flask(__name__)
app.secret_key = b'23333'

@app.route('/')
def index():
    return 'nice' if is_login() else ('未登录', 400)

@app.route('/check_ts/')
def check_ts():
    ts = request.args.get('ts', None)
    username = request.args.get('username', None)
    if ts == get_ts(username):
        return jsonify({'username': username})
    else:
        return jsonify({}), 400

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
            <form action="/login/" method="post">
                <label for="">账号<input type="text" name="username"></label>
                <label for="">密码<input type="text" name="password"></label>
                <input type="submit" name="" value="登录">
            </form>
        '''
    else:
        if not is_login():
            username = request.form['username']
            pwd = request.form['password']
            if test_users.get(username, {}).get('pwd') != pwd:
                return '登录失败，账号或密码错误', 400
            session['username'] = username
        import pdb;pdb.set_trace()
        print(request.args)
        return_url = request.args.get('return_url', None)
        return_path = request.args.get('return_path', None)
        print(return_url, return_path)
        username = session.get('username')
        if not return_url:
            return '登录成功'
        ts = set_ts(username, return_url)
        return redirect(f'{return_url}login/?ts={ts}&username={username}&return_path={return_path}')


@app.route('/logout/', methods=['get'])
def logout():
    username = session.pop('username', None)
    clear_ts(username)
    return 'logout'

if __name__ == "__main__":
    app.run(port=9999)
