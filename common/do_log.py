"""
@Time    : 2019/4/30 0030 15:59
@Author  : Cooper
@File    : do_log.py
@Function: 完成日志收集
"""
import logging
from common import contants
from common.config import config

class MyLog:
    def __init__(self, log_name):
        self.log_name = log_name  # 日志收集器名字

    def my_log(self):
        my_log = logging.getLogger(self.log_name)
        my_log.setLevel('DEBUG')
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s : %(lineno)d] - %(message)s')
        fh = logging.FileHandler(contants.log_file, encoding='utf-8')
        fh.setLevel(config.get_value('log', 'fhlevel'))
        fh.setFormatter(formatter)

        ch = logging.StreamHandler()
        ch.setLevel(config.get_value('log', 'chlevel'))
        ch.setFormatter(formatter)

        my_log.addHandler(ch)
        my_log.addHandler(fh)

        return my_log


if __name__ == '__main__':
    pass