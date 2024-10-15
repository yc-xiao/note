from random import randint, sample
from functools import wraps
from . import logger
import os

def pdb(func, *args, **kwargs):
    breakpoint()
    result = func(*args, **kwargs)
    logger.info(result)
    return result


def _safe_get(obj, *args, const=''):
    for arg in args:
        obj = getattr(obj, arg, const)
        if obj == const:
            return obj
    return obj


def _rm(path):
    '''删除目录或文件'''
    if os.path.isdir(path):
        for sp in os.listdir(path):
            _rm(os.path.join(path, sp))
        if os.path.exists(path):
            os.rmdir(path)
    else:
        if os.path.exists(path):
            os.remove(path)


def safe_get(obj, chain, default='', const=''):
    # example: sample.project.id， safe_get(sample, 'project.id', 1)
    value = _safe_get(obj, *chain.split('.'), const=const)
    return value if value != const else default

def get_random(n=6, t='num'):
    if t == 'chr':
        k = [chr(letter) for letter in range(65, 91)]
        return ''.join(sample(k, n))
    return str(randint(10**(n-1), 10**n - 1))

def generate_number(n, bit=5):
    n = str(n)
    return (bit - len(n)) * '0' + n

def get_traceback_info(e, tb=None, format='str'):
    tb = tb or e.__traceback__
    code, f_locals = tb.tb_frame.f_code, tb.tb_frame.f_locals
    traceback_info = {'filename': code.co_filename, 'line_no': tb.tb_lineno, 'error': str(e),
                      'func_name': code.co_name, 'f_locals': str(f_locals)}
    if format == 'str':
        return 'location:{filename}:{line_no};\nfunction:{func_name}, f_locals:{f_locals};\nerror_message: {error}。'.format(**traceback_info)
    return traceback_info

def try_err(email=True, log=True, msg='错误信息', raise_error=False):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                if log:
                    logger.debug(f'{func.__name__} 启动')
                result = func(*args, **kwargs)
                if log:
                    logger.debug(f'{func.__name__} 完成')
                return result
            except Exception as e:
                info = get_traceback_info(e, e.__traceback__.tb_next)
                if email:
                    logger.error(info)
                else:
                    logger.warning(info)
                # 上抛错误，当return None时，上级函数处理异常，会覆盖原有的错误
                if raise_error:
                    raise e
        return inner
    return wrapper