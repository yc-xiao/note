from werkzeug.wrappers import Response
from werkzeug.serving import make_server

from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule, NotFound, RequestRedirect

@Request.application
def application(request):
    return Response("Hello %s!" % request.args.get('name', 'World!'))


def app(environ, start_response):
    response = Response('Hello World!', mimetype='text/plain')
    return response(environ, start_response)

httpd = make_server(host='127.0.0.1', port=8888, app=application)
httpd.serve_forever()
