from werkzeug.serving import make_server

def application(environ, start_response):
    doc = 'environ请求的环境变量，start_response响应头设置，只调用一次'
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b'Helloc']

httpd = make_server('127.0.0.1', 8888, application)
httpd.serve_forever()
