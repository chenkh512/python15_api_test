"""
@Time    : 2019/5/2 22:18
@Author  : Cooper
@File    : do_re.py
@Function:
"""

import re
from common.config import config
import configparser
from common.do_log import MyLog


class Context:
    """
    设定反射的类
    """
    code = None
    register_mobile = None
    register_ip = None
    register_name = None
    time_out_code = None
    time_out_mobile = None
    auth_uid = None
    not_auth_uid = None
    second_code = None
    auth_id = None
    auth_name = None


def DoRe(data):
    """
    1.用正则表达式来匹配测试数据中的指定字符
    2.根据指定字符获取到配置文件中对应的值
    3.然后进行替换
    """
    pattern = '#(.*?)#'  # 正则表达式   匹配组当中多次或者最多一次单个字符

    while re.search(pattern, data):
        search = re.search(pattern, data)  # 从任意位置开始找，找第一个就返回Match object, 如果没有找None
        group = search.group(1)  # 拿到参数化的KEY

        try:
            value = config.get_value('data', group)  # 根据KEY取配置文件里面的值
        except configparser.NoOptionError as e:  # 如果配置文件里面没有的时候，去do_re模块中类Context里面取
            if hasattr(Context, group):  # 判断类属性名是否在Context中
                value = getattr(Context, group)  # 获取类属性值
            else:
                MyLog(__name__).my_log().error('找不到参数化的值', e, exc_info=True)
                raise e

        """
        记得替换后的内容，继续用data接收
        """
        data = re.sub(pattern, value, data, count=1)  # 查找替换,count查找替换的次数

    return data
