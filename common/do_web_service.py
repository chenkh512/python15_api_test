"""
@Time    : 2019/4/28 0028 16:33
@Author  : Cooper
@File    : web-service.py
@Function: 完成webservice接口请求
"""

from suds.client import Client
from common.config import config
from common.do_log import MyLog


class WebService:
    mylog = MyLog(__name__).my_log()

    def web_service(self, url, data, function_name):

        if type(data) == str:
            data = eval(data)

        url = config.get_value('api', 'base_url') + url

        self.mylog.debug('请求的接口函数：{}'.format(function_name))
        self.mylog.debug('请求的地址：{}'.format(url))
        self.mylog.debug('请求的数据：{}'.format(data))

        try:
            if hasattr(Client(url).service, function_name):
                client = Client(url).service.__getattr__(function_name)
                try:
                    result = client(data)
                    resp = result.retInfo
                    self.mylog.info('返回的结果 {}'.format(resp))
                    return resp

                except Exception as e:
                    resp = str((e.__dict__)['fault'].faultstring)
                    self.mylog.info('返回的结果 {}'.format(resp))
                    return resp
        except Exception as e:
            self.mylog.error('没有这个接口函数，报错信息: {}'.format(e))
            raise e


if __name__ == '__main__':
    a = WebService()
    # sendcode = a.web_service('sms-service-war-1.0/ws/smsFacade.ws?wsdl',
    #                          {"client_ip": "192", "tmpl_id": "1", "mobile": "15884452586"}, 'sendMCode')
    # print(sendcode)
    # #
    # register = a.web_service('finance-user_info-war-1.0/ws/financeUserInfoFacade.ws?wsdl',
    #                          {"verify_code": "662157", "user_id": "Co11per", "channel_id": "3", "pwd": "1234567",
    #                           "mobile": "15884452586", "ip": ""},
    #                          'userRegister')
    # print(register)

    # auth = a.web_service('finance-user_info-war-1.0/ws/financeUserInfoFacade.ws?wsdl',
    #                      {"uid": "100009744", "true_name": "周是", "cre_id": "510922198902080059"}, 'verifyUserAuth')
    # print(auth)
    # url='http://120.24.235.105:9010/finance-user_info-war-1.0/ws/financeUserInfoFacade.ws?wsdl'
    # client = Client(url)
    # print(client)

    bank = a.web_service('finance-user_info-war-1.0/ws/financeUserInfoFacade.ws?wsdl',
                         {"uid": "100009769", "pay_pwd": "123456", "mobile": "15375104207",
                          "cre_id": "362426200108261321", "user_name": "张明", "cardid": "6217003810026896707",
                          "bank_type": "1001", "bank_name": ""}, 'bindBankCard')
    print(bank)
    # url='http://120.24.235.105:9010/finance-user_info-war-1.0/ws/financeUserInfoFacade.ws?wsdl'
    # client = Client(url)
    # print(client)
    #
    # 修改密码
    # change = a.web_service('finance-user_info-war-1.0/ws/financeUserInfoFacade.ws?wsdl',
    #                        {"uid": "100009749", 'old_pay_pwd': '123456', 'new_pay_pwd': '123456',
    #                         'paypwd_ip': '192.168.150.171'}, 'changePayPwd')
    # print(change)

    # import random,string
    # print(random.sample('zyxwvutsrqponmlkjihgfedcba', 5))
    #
    # ran_str = ''.join(random.sample(string.ascii_letters, 6))
    # print(ran_str.lower())
    #
    # print(''.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a'], 5)))
    # import hashlib
    # # 待加密信息
    # r_mobile = '15884567545'
    #
    # # 创建md5对象
    # hl = hashlib.md5()
    # # print(hl)
    # # 此处必须声明encode
    # # 若写法为hl.update(str)  报错为： Unicode-objects must be encoded before hashing
    # hl.update(r_mobile.encode(encoding='utf-8'))
    # #
    # #
    # print('MD5加密后为 ：' + hl.hexdigest())
    # import random
    #
    # f_name = ['张', '金', '李', '王', '赵', '熊', '纪', '舒', '屈', '项', '祝', '董', '梁']
    #
    # m_name = ['玉', '明', '龙', '芳', '军', '玲', '乾', '坤',]
    #
    # l_name = ['', '立', '玲', '', '国', '']
    #
    # for i in range(1):
    #     auth_name = random.choice(f_name) + random.choice(m_name) + random.choice(l_name)
    #     print(auth_name)
    # import random, string
    #
    # random_phone = '621700381' + ''.join(random.sample(string.digits, 10))
    # print(random_phone)
