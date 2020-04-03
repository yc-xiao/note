"""
    handler_time:
        返回时间区间
    args:
        cur_time 指定时间点
        period  时间间隔 day, week(只返回时间点当月所有周), month
        step 指定区间大小，不适用与week
        reversed 默认从当前向过去取值
    return:
        []
"""

from datetime import datetime, timedelta
from faker import Factory
from random import choice

def handler_time(cur_time=None, period=None, step=None, reversed=False):
    result = []

    if not cur_time:
        cur_time = datetime.now()

    if isinstance(cur_time, str):
        date_strs = ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d')
        for date_str in date_strs:
            try:
                cur_time = datetime.strptime(cur_time, date_str)
                break
            except:
                continue

    if not isinstance(cur_time, datetime):
        return result

    if not step:
        # 默认天数按7天算，月数按半年算
        step = 7 if period == 'day' else 6

    result.append(cur_time)
    cur_time = cur_time.date()
    if period == 'day':
        # 天 间隔为7天
        for i in range(0, step):
            result.append(cur_time-timedelta(i))

    elif period == 'week':
        # 周　返回该月所有周
        result = []
        year, month = cur_time.year, cur_time.month
        temp_day = 1

        temp_time = datetime(year=year, month=month, day=temp_day)
        result.append(temp_time)
        temp_day = temp_day - temp_time.weekday() + 7
        count = 10
        while count>0:
            try:
                result.append(datetime(year=year, month=month, day=temp_day))
                temp_day += 7
            except:
                break
            count-=1
        else:
            return []
        if month==12:
            result.append(datetime(year=year+1, month=1, day=1))
        else:
            result.append(datetime(year=year, month=month+1, day=1))
        result = result[::-1]

    elif period == 'month':
        # 月　间隔为6个月
        year, month = cur_time.year, cur_time.month
        if month > 5:
            for i in range(0, step):
                result.append(datetime(year=year, month=month-i, day=1))
        else:
            for i in range(0, step):
                if month-i > 0:
                    result.append(datetime(year=year, month=month-i, day=1))
                else:
                    result.append(datetime(year=year-1, month=month-i+12, day=1))

    if reversed:
        result = result[::-1]
    return result

def test():
    periods = ['day', 'week', 'month']
    fake = Factory.create()
    for i in range(10):
        period = choice(periods)
        cur_time = fake.date_time()
        result = handler_time(cur_time=cur_time, period=period)
        print(f'''第{i}次测试结果:
            period:{period}, datetime:{cur_time}
            result:{result}
            ''')

if __name__ == '__main__':
    test()
