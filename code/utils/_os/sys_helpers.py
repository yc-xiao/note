"""
    linux系统操作命令
"""
from colorlog import ColoredFormatter
import subprocess
import logging
import shutil
import json
import os


def setup_logger(name, level=logging.DEBUG):
    """Return a logger with a default ColoredFormatter."""
    formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - p%(process)s - {%(filename)s:%(lineno)d} - %(levelname)s - %(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'red',
        }
    )
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger


sys_logger = setup_logger('system_operator_logger')


class SystemOperator(object):
    unit_map = {'KB': 1024, 'MB': 1024 ** 2, 'GB': 1024 ** 3, 'TB': 1024 **4}
    mountpoint_root = '/mnt'

    def run(self, cmd):
        # 返回 stdout, stderror
        cmd = cmd.split(' ')
        cmd = [_ for _ in cmd if _]  # 过滤多余空格
        sys_logger.info(f'执行命令: {cmd}')
        try:
            # 每次调用该方法都会启动一个新的进程，可以考虑使用更基础的subprocess.Popen
            response = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                      universal_newlines=True, timeout=10)
            stdout, stderr, return_code = response.stdout, response.stderr, response.returncode
            if return_code != 0 or stderr:
                raise Exception(stderr)
            sys_logger.info(f'命令 {cmd} 执行结果 {stdout}')
            return stdout, None
        except Exception as e:
            sys_logger.error(f'命令 {cmd} 执行错误信息: {e}')
            return None, e

    def mount(self, mountpoint, directory_path, username=None, password=None):
        mountpoint = os.path.join(self.mountpoint_root, mountpoint)
        if not os.path.exists(mountpoint):
            os.mkdir(mountpoint)
        if self.is_mounted(mountpoint):
            raise Exception(f'挂载失败， 挂载点: {mountpoint}已挂载!')
        cmd = f'mount -o noperm {directory_path} {mountpoint}'
        if username and password:
            cmd = f'{cmd} -o username={username},password={password}'

        stdout, stderr = self.run(cmd)
        if stderr:
            raise Exception(f'挂载失败， 失败原因{stderr.args}')

    def umount(self, mountpoint):
        mountpoint = os.path.join(self.mountpoint_root, mountpoint)
        cmd = f'umount {mountpoint}'
        stdout, stderr = self.run(cmd)
        if stderr:
            raise Exception(f'卸载失败，　失败原因{stderr.args}')

    def make_archive(self, base_name, root_dir, format='gztar'):
        # base_name 压缩后文件名
        # root_dir  压缩文件所在路径
        sys_logger.info(f'将目录 {root_dir} 归档到 {base_name}')
        if not os.path.exists(root_dir):
            raise Exception(f'目录不存在{root_dir}!')
        return shutil.make_archive(base_name, format, root_dir)

    def is_mounted(self, dir):
        # 目录是否挂载
        cmd = f'mountpoint {dir}'
        stdout, stderr = self.run(cmd)
        if stdout:
            return True

    def getsize(self, path, unit='KB'):
        # 获取文件或目录大小
        # 空文件与浮点数存在计算误差, 文件体积大可忽略误差
        size = self._getsize(path)
        unit_num = self.unit_map.get(unit, 1)
        return size/unit_num

    def disk_usage(self, path, unit='KB'):
        total, used, free = self._disk_usage(path)
        unit_num = self.unit_map.get(unit, 1)
        return {'total': total/unit_num, 'used': used/unit_num, 'free': free/unit_num, 'unit': unit}

    def rm(self, path):
        # 只运行删除/Data/目录下的文件
        if r'/Data/' not in path:
            raise Exception(f'{path}不在/Data/下，不允许删除!')
        if not os.path.exists(path):
            return
        if os.path.isdir(path):
            self._rmdir(path)
        else:
            self._rmfile(path)

    def ls_umount_disk(self, *args, **kw):
        cmd = 'lsblk -JO'
        stdout, stderr = self.run(cmd)
        if stderr:
            raise stderr
        data = json.loads(stdout)
        return data['blockdevices']

    def _getsize(self, path):
        if os.path.isfile(path):
            size = os.path.getsize(path)
        else:
            size = 4 * 1024  # 空文件夹默认4KB
            for _ in os.listdir(path):
                new_path = os.path.join(path, _)
                size += self._getsize(new_path)
        return size

    def _rmdir(self, path):
        shutil.rmtree(path)

    def _rmfile(self, path):
        os.remove(path)

    def _disk_usage(self, path):
        return shutil.disk_usage(path)

    def change_size(self, size, unit='KB', to_unit=None):
        unit_num = self.unit_map.get(unit)
        size = size * unit_num  # 转换为字节B
        unit_array = ['B', 'KB', 'MB', 'GB', 'TB']

        index = 0
        while size > 1024:
            size /= 1024
            index += 1
        if size:
            size = int(size) + 1  # 向上取整
        return f'{size}{unit_array[index]}'


sys_operator = SystemOperator()