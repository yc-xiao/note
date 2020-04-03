'''
    WSGI协议
    def application(env, start_response):
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return ['Helloc']
'''
from werkzeug.serving import run_simple
import pdb
import os

def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b'Helloc']

BASE_PATH = os.path.dirname(os.path.dirname(__file__))
BASE_STATIC = os.path.join(BASE_PATH, 'static')

config = {
    'hostname': '127.0.0.1',
    'port': 8888,
    'use_debugger': True,
    'use_reloader': True,
    'static_files': {
        '/static': BASE_STATIC
    },
    'application': application,
}
run_simple(**config)
