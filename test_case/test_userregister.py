"""
@Time    : 2019/4/30 0030 17:27
@Author  : Cooper
@File    : test_userregister.py
@Function: 完成注册接口
"""

import unittest, string, random, json
from ddt import ddt, data
from common.do_web_service import WebService
from common.do_excel import Do_excel
from common import contants
from common.do_mysql import DoMysql
from common.do_log import MyLog
from common.do_re import DoRe
from common.do_re import Context


@ddt
class TestUserRegister(unittest.TestCase):
    doexcel_ob = Do_excel(contants.case_file, 'userRegister')
    mylog = MyLog(__name__).my_log()

    @classmethod
    def setUpClass(cls):
        cls.service = WebService()
        cls.mysql = DoMysql()
        cls.mylog.info('开始执行用例')

    @data(*doexcel_ob.get_data())
    def test_userregister(self, case):

        case.data = DoRe(case.data)

        # 随机生成IP地址，并且反射到Context类的属性中，方便后面参数调用
        if case.data.find('register_ip') != -1:
            random_ip = '192.168.1' + ''.join(random.sample(string.digits, 2)) + '.1' + ''.join(
                random.sample(string.digits, 2))
            setattr(Context, 'register_ip', random_ip)
            case.data = case.data.replace('register_ip', random_ip)

        # 随机生成用户名，并且反射到Context类的属性中，方便后面参数调用
        if case.data.find('register_name') != -1:
            random_str = ''.join(random.sample(string.ascii_letters, 6))
            case.data = case.data.replace('register_name', random_str.lower())
            setattr(Context, 'register_name', random_str)

        # 随机生成电话号码，并且反射到Context类的属性中，方便后面参数调用
        random_phone = '15' + ''.join(random.sample(string.digits, 6)) + '207'
        if case.data.find('register_mobile') != -1:
            setattr(Context, 'register_mobile', random_phone)
            case.data = case.data.replace('register_mobile', random_phone)

        # 替换sql中指定的值
        if case.sql is not None and case.sql.find('register_mobile') != -1:
            case.sql = case.sql.replace('register_mobile', random_phone)

        # 查询数据库，并且把查询的结果反射到Context类的属性中，方便后面参数调用
        if case.case_id == 4 and case.sql is not None:
            sql = json.loads(case.sql)['sql_4']
            time_out_code = self.mysql.fetch_one(sql)['Fverify_code']
            setattr(Context, 'time_out_code', time_out_code)
            time_out_mobile = self.mysql.fetch_one(sql)['Fmobile_no']
            setattr(Context, 'time_out_mobile', time_out_mobile)

        self.mylog.debug('第 {} 条用例'.format(case.case_id))
        self.mylog.debug('用例名称：{}'.format(case.case_name))
        resp = self.service.web_service(url=case.url, data=case.data, function_name=case.function_name)
        self.mylog.debug('预期结果：{}'.format(case.expected))

        # 查询数据库，并且把查询的结果反射到Context类的属性中，方便后面参数调用
        if case.case_id == 1 and resp == 'ok':
            sql = json.loads(case.sql)['sql_1']
            code = self.mysql.fetch_one(sql)['Fverify_code']
            setattr(Context, 'code', code)

        try:
            self.assertEqual(case.expected, resp)
            self.doexcel_ob.write_data(case.case_id + 1, resp, 'PASS')
        except AssertionError as e:
            self.doexcel_ob.write_data(case.case_id + 1, resp, 'FAIL')
            self.mylog.error('断言出错啦! {}'.format(e))
            raise e

    @classmethod
    def tearDownClass(cls):
        cls.mysql.close()

        cls.mylog.info('用例执行完毕')
