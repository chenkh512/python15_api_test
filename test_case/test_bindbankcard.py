"""
@Time    : 2019/5/4 13:59
@Author  : Cooper
@File    : test_bindbankcard.py
@Function: 完成银行卡绑定
"""

import unittest, string, random, json, time
from ddt import ddt, data
from common.do_web_service import WebService
from common.do_excel import Do_excel
from common import contants
from common.do_mysql import DoMysql
from common.do_log import MyLog
from common.do_re import DoRe
from common.do_re import Context
from datetime import timedelta, date


@ddt
class TestBindBankCard(unittest.TestCase):
    doexcel_ob = Do_excel(contants.case_file, 'bindBankCard')
    mylog = MyLog(__name__).my_log()

    @classmethod
    def setUpClass(cls):
        cls.service = WebService()
        cls.mysql = DoMysql()
        cls.mylog.info('开始执行用例')

    @data(*doexcel_ob.get_data())
    def test_bindbankcard(self, case):

        case.data = DoRe(case.data)

        # 随机生成IP地址，并且反射到Context类的属性中，方便后面参数调用
        if case.data.find('register_ip') != -1:
            random_ip = '192.168.1' + ''.join(random.sample(string.digits, 2)) + '.1' + ''.join(
                random.sample(string.digits, 2))
            setattr(Context, 'register_ip', random_ip)
            case.data = case.data.replace('register_ip', random_ip)

        # 随机生成用户名，并且反射到Context类的属性中，方便后面参数调用
        random_str = ''.join(random.sample(string.ascii_letters, 6))
        if case.data.find('register_name') != -1:
            case.data = case.data.replace('register_name', random_str.lower())
            setattr(Context, 'register_name', random_str)

        # 替换sql中指定的值
        if case.sql is not None and case.sql.find('register_name') != -1:
            case.sql = case.sql.replace('register_name', random_str)

        # 随机生成电话号码，并且反射到Context类的属性中，方便后面参数调用
        random_phone = '15' + ''.join(random.sample(string.digits, 6)) + '207'
        if case.data.find('register_mobile') != -1:
            setattr(Context, 'register_mobile', random_phone)
            case.data = case.data.replace('register_mobile', random_phone)

        # 随机生成银行卡号
        if case.data.find('card_id') != -1:
            id_code_list = [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
            AAA = random.randint(0, 999)
            BBB = random.randint(0, 999)
            CCC = random.randint(0, 999999)
            result = '621700' + str(AAA).zfill(3) + str(BBB).zfill(3) + str(CCC).zfill(6)
            random_cardid = result + str(sum([a * b for a, b in zip(id_code_list, [int(a) for a in result])]) % 10)
            case.data = case.data.replace('card_id', random_cardid)

        # 替换sql中指定的值
        if case.sql is not None and case.sql.find('register_mobile') != -1:
            case.sql = case.sql.replace('register_mobile', Context.register_mobile)

        # 随机生成姓名
        f_name = ['张', '金', '李', '王', '赵', '熊', '纪', '舒', '屈', '项', '祝', '董', '梁']
        m_name = ['玉', '明', '龙', '芳', '军', '玲', '乾', '坤', ]
        l_name = ['', '立', '玲', '', '国', '']
        for i in range(1):
            auth_name = random.choice(f_name) + random.choice(m_name) + random.choice(l_name)
            if case.data.find('auth_name') != -1:
                case.data = case.data.replace('auth_name', auth_name)
                setattr(Context, 'auth_name', auth_name)

        # 随机生成身份证号码
        first_list = ['362402', '362421', '362422', '362423', '362424', '362425', '362426', '362427', '362428',
                      '362429',
                      '362430', '362432', '110100', '110101', '110102', '110103', '110104', '110105', '110106',
                      '110107',
                      '110108', '110109', '110111']

        id_code_list = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        check_code_list = [1, 0, 'X', 9, 8, 7, 6, 5, 4, 3, 2]

        area_code = random.choice(first_list)
        datestring = str(date(int(time.strftime('%Y')) - 18, 1, 1) + timedelta(days=random.randint(0, 364))).replace(
            "-", "")
        rd = random.randint(0, 999)
        result = str(area_code) + datestring + str(rd).zfill(3)
        auth_id = result + str(
            check_code_list[sum([a * b for a, b in zip(id_code_list, [int(a) for a in result])]) % 11])
        if case.data.find('auth_id') != -1:
            case.data = case.data.replace('auth_id', auth_id)
            setattr(Context, 'auth_id', auth_id)

        self.mylog.debug('第 {} 条用例'.format(case.case_id))
        self.mylog.debug('用例名称：{}'.format(case.case_name))
        resp = self.service.web_service(url=case.url, data=case.data, function_name=case.function_name)
        self.mylog.debug('预期结果：{}'.format(case.expected))

        # 查询数据库，并且把查询的结果反射到Context类的属性中，方便后面参数调用
        if case.case_id == 3 and resp == 'ok':
            sql = json.loads(case.sql)['sql_3']
            code = self.mysql.fetch_one(sql)['max(Fuid)']
            setattr(Context, 'not_auth_uid', str(code + 1))

        # 查询数据库，并且把查询的结果反射到Context类的属性中，方便后面参数调用
        if case.case_id == 1 and resp == 'ok':
            sql = json.loads(case.sql)['sql_1']
            code = self.mysql.fetch_one(sql)['Fverify_code']
            setattr(Context, 'code', code)

        # 查询数据库，并且把查询的结果反射到Context类的属性中，方便后面参数调用
        if case.case_id == 2 and resp == 'ok':
            sql = json.loads(case.sql)['sql_2']
            code = self.mysql.fetch_one(sql)['Fuid']
            setattr(Context, 'auth_uid', str(code))

        if case.case_id == 4 and resp == 'ok':
            sql = json.loads(case.sql)['sql_4']
            code = self.mysql.fetch_one(sql)['Fverify_code']
            setattr(Context, 'second_code', code)

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
