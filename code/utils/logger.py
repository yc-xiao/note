import logging
def get_logger(name='test'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # 设置全局log级别为debug。注意全局的优先级最高

    hterm = logging.StreamHandler()  # 创建一个终端输出的handler,设置级别为error
    hterm.setLevel(logging.DEBUG)

    hfile = logging.FileHandler("access.log")  # 创建一个文件记录日志的handler,设置级别为info
    hfile.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # 创建一个全局的日志格式

    hterm.setFormatter(formatter)  # 将日志格式应用到终端handler
    hfile.setFormatter(formatter)  # 将日志格式应用到文件handler

    logger.addHandler(hterm)  # 将终端handler添加到logger
    logger.addHandler(hfile)  # 将文件handler添加到logger

    return logger


logger = get_logger('script')

def test():
    logger.info('helloc')
    logger.error('error')

test()