"""
@Time    : 2019/4/30 0030 11:14
@Author  : Cooper
@File    : config.py
@Function: 完成配置文件的读取
"""
import configparser
from common import contants


class Config:
    """
    通过配置文件来切换环境
    """
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(contants.global_file, encoding='utf-8')

        if self.config.getboolean('switch', 'on'):
            self.config.read(contants.test_file, encoding='utf-8')
        else:
            self.config.read(contants.staging_file, encoding='utf-8')

    def get_value(self, section, option):
        return self.config.get(section, option)


config = Config()
