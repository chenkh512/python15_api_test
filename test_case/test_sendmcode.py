"""
@Time    : 2019/4/29 0029 17:20
@Author  : Cooper
@File    : test_sendmcode.py
@Function: 完成短信验证码接口
"""
import unittest, string, random, json
from ddt import ddt, data
from common.do_web_service import WebService
from common.do_excel import Do_excel
from common import contants
from common.do_mysql import DoMysql
from common.do_log import MyLog


@ddt
class TestSendMCode(unittest.TestCase):
    doexcel_ob = Do_excel(contants.case_file, 'sendMCode')
    mylog = MyLog(__name__).my_log()

    @classmethod
    def setUpClass(cls):
        cls.service = WebService()
        cls.mysql = DoMysql()
        cls.mylog.info('开始执行用例')

    @data(*doexcel_ob.get_data())
    def test_sendmcode(self, case):

        # 随机生成IP地址，并且反射到Context类的属性中，方便后面参数调用
        if case.data.find('sendmcode_ip') != -1:
            random_ip = '192.168.1' + ''.join(random.sample(string.digits, 2)) + '.1' + ''.join(
                random.sample(string.digits, 2))
            case.data = case.data.replace('sendmcode_ip', random_ip)

        # 随机生成电话号码，并且反射到Context类的属性中，方便后面参数调用
        random_phone = '15' + ''.join(random.sample(string.digits, 6)) + '207'
        if case.data.find('sendmcode_mobile') != -1:
            case.data = case.data.replace('sendmcode_mobile', random_phone)

        # 替换sql中指定的值
        if case.sql is not None and case.sql.find('sendmcode_mobile') != -1:
            case.sql = case.sql.replace('sendmcode_mobile', random_phone)

        self.mylog.debug('第 {} 条用例'.format(case.case_id))
        self.mylog.debug('用例名称：{}'.format(case.case_name))
        resp = self.service.web_service(url=case.url, data=case.data, function_name=case.function_name)
        self.mylog.debug('预期结果：{}'.format(case.expected))

        # 查询数据库，验证影响的行数
        if case.sql is not None:
            sql = json.loads(case.sql)['sql_1']
            result = self.mysql.fetch_one(sql)
            self.mylog.info('数据库查询结果 {}'.format(result))

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
