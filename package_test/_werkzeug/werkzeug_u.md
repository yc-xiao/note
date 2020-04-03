## werkzeug
> - WSGI
>> Werkzeug 是一个 WSGI 工具包。
>> WSGI 是一个 Web 应用和服务器通信的协议。两部分application和server，其中application规定为可调用对象需要传入两个参数，返回一个可迭代对象。
>> ```python
from werkzeug.serving import make_server
doc = 'environ请求的环境变量，start_response响应头设置，只调用一次'
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b'Helloc']
httpd = make_server('127.0.0.1', 8888, application)
httpd.serve_forever()
```
> - HTTP服务
```
run_simple
    -> (socket/inner)
    -> inner -> make_server
        -> ThreadedWSGIServer(ThreadingMixIn，BaseWSGIServer)
        -> ForkingWSGIServer(ForkingMixIn，BaseWSGIServer)
        -> BaseWSGIServer(HTTPServer)
            -> ThreadingMixIn，ForkingMixIn ->
            -> HTTPServer，WSGIRequestHandler -> (BaseHTTPServer/http.server)
                -> SocketServer
例子 run_simple -> socket
例子 run_simple -> inner -> make_server -> BaseWSGIServer -> HTTPServer-> BaseHTTPServer ->>SocketServer -> Socket
```


> - 流程分析
>> make_server -> BaseWSGIServer(HTTPServer)实例 -> TCPServer ->
BaseServer(整个连接过程会有一个handler代理处理数据传输处理)
>>1.make_server()，返回一个BaseWSGIServer实例。
>>2.BaseWSGIServer类内关联一个WSGIRequestHandler，WSGIRequestHandler封装请求并处理数据，以及实现WSGI。
>>3.WSGIRequestHandler->BaseHTTPRequestHandler->StreamRequestHandler->BaseRequestHandler，BaseRequestHandler初始化时，执行(self.setup(),self.handle(),self.finish())
StreamRequestHandler重写(self.setup(),self.finish())
BaseHTTPRequestHandler重写(self.handle())，handle将socket封装成http并调用应用
>>4.BaseWSGIServer->HTTPServer->TCPServer->BaseServer
BaseServer实现serve_forever监听，接收到socket请求依次处理
_handle_request_noblock，process_request，finish_request，shutdown_request.
其中finish_request实例化WSGIRequestHandler，WSGIRequestHandler通过handle->handle_one_request->parse_request(获取请求地址等)->run_wsgi(安装wsgi协议处理数据)

---
#### [参考](https://www.kancloud.cn/manual/werkzeug/71003)
