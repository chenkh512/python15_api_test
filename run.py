"""
@Time    : 2019/5/4 23:28
@Author  : Cooper
@File    : run.py.py
@Function: 执行测试用例
"""

import sys

sys.path.append('./')  # project 的根目录地址

import unittest, HTMLTestRunnerNew
from common import contants

# 识别文件下带有test_开头的文件
discover = unittest.defaultTestLoader.discover(contants.discover_file, pattern='test*.py')

with open(contants.report_file, 'wb') as file:
    runner = HTMLTestRunnerNew.HTMLTestRunner(stream=file, title='WebService_test',
                                              description='WebService接口自动化测试报告', tester='Cooper')
    runner.run(discover)
