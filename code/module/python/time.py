from datetime import datetime, timedelta
from django.utils import timezone
from functools import wraps
from .logger import logger

import pytz
import time

USE_TZ = True
UTC_TZ = pytz.timezone('UTC')
LOCAL_TZ = pytz.timezone('Asia/Shanghai')
FMT = '%Y-%m-%d %H:%M:%S'
FMT2 = '%Y%m%d%H%M%S'


def datetime_to_str(obj:datetime=None, fmt=FMT, tz=LOCAL_TZ):
    if not isinstance(obj, datetime):
        return ''
    # astimezone(tz)，将日期转到指定时区。若时区不一致，则日期发生变化。
    return obj.strftime(fmt) if timezone.is_naive(obj) else obj.astimezone(tz).strftime(fmt)


def str_to_datetime(stime:str='', tz=LOCAL_TZ):
    if not stime:
        return None
    formats = [FMT, '%Y-%m-%d %H:%M', '%Y-%m-%d', '%Y/%m/%d %H:%M:%S', '%Y/%m/%d %H:%M']
    for fmt in formats:
        try:
            obj = datetime.strptime(stime, fmt)
            if USE_TZ:
                # 时区：当前生成的时间与指定时区生成的时间存在偏差，通过localize进行调整
                obj = tz.localize(obj)
            return obj
        except ValueError:
            continue

def get_now(tz=LOCAL_TZ):
    return datetime.now(tz)

def get_now_str(fmt=FMT):
    return datetime_to_str(get_now(), fmt)


def check_time_range(min_time='', max_time='', days=31):
    if not isinstance(min_time, datetime):
        min_time = str_to_datetime(min_time)
    if not isinstance(max_time, datetime):
        max_time = str_to_datetime(max_time)
    assert min_time and max_time, '日期的最小值或最大值不允许为空'
    assert min_time <= max_time, '日期的最小值必须小于最大值'
    return min_time, max_time


def get_step_time_list(min_time, max_time, step='month', strtime=None):
    if not isinstance(min_time, datetime) or not isinstance(max_time, datetime) or \
       step not in ['day', 'month', 'year']:
        raise Exception('参数错误!')
    if not strtime:
        step_strtime_dic = {'day': '%Y-%m-%d', 'month': '%Y-%m', 'year': '%Y'}
        strtime = step_strtime_dic[step]
    max = max_time.strftime(strtime)
    min = min_time.strftime(strtime)

    times = []
    while min_time < max_time:
        times.append(min)
        if step == 'day':
            min_time = min_time + timedelta(days=1)
        elif step == 'year':
            min_time = datetime(year=min_time.year+1, month=min_time.month, day=min_time.day)  # noqa: E501
        else:
            if min_time.month == 12:
                min_time = datetime(year=min_time.year + 1, month=1, day=1)
            else:
                min_time = datetime(year=min_time.year, month=min_time.month+1, day=1)

        min = min_time.strftime(strtime)
    times.append(max)
    return times


def sec_to_time(sec):
    d = datetime(1,1,1) + timedelta(seconds=sec)
    s = ''
    if d.hour:
        s += f'{d.hour}h'
    if d.minute:
        s += f'{d.minute}m'
    if d.second:
        s += f'{d.second}s'
    return s


def duration(show_arg=True):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            t = time.time()
            if show_arg:
                logger.info(f'开始{func.__module__}.{func.__name__}，参数:{args}, {kwargs}')
            else:
                logger.info(f'开始{func.__module__}.{func.__name__}')
            result = func(*args, **kwargs)
            logger.info(f'结束{func.__module__}.{func.__name__}，运行时间:{sec_to_time(time.time()-t)}')
            return result
        return inner
    return wrapper