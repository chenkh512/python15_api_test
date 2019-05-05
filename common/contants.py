"""
@Time    : 2019/4/29 0029 16:34
@Author  : Cooper
@File    : contants.py
@Function: 完成文件路径配置
"""
import os

# base_dir = os.path.abspath('../')
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

case_file = os.path.join(base_dir, 'test_data', 'case.xlsx')


global_file = os.path.join(base_dir, 'conf', 'global.conf')

test_file = os.path.join(base_dir, 'conf', 'test.conf')

staging_file = os.path.join(base_dir, 'conf', 'staging.conf')

log_file = os.path.join(base_dir, 'test_report', 'report.txt')

discover_file = os.path.join(base_dir, 'test_case')

report_file = os.path.join(base_dir, 'test_report', 'report.html')
