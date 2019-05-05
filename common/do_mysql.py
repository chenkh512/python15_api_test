"""
@Time    : 2019/4/30 0030 10:12
@Author  : Cooper
@File    : do_mysql.py
@Function: 完成数据库的操作
"""

import pymysql
from common.config import config


class DoMysql:
    def __init__(self):
        self.mysql = pymysql.Connect(host=config.get_value('testdb', 'host'),
                                     port=int(config.get_value('testdb', 'port')),
                                     user=config.get_value('testdb', 'user'),
                                     password=config.get_value('testdb', 'password'),
                                     charset=config.get_value('testdb', 'charset'),
                                     )
        self.cursor = self.mysql.cursor(cursor=pymysql.cursors.DictCursor)  # 以字典格式返回查询的结果
        # self.cursor = self.mysql.cursor()  # 以元组格式返回查询的结果

    def fetch_one(self, sql):
        self.cursor.execute(sql)
        self.mysql.commit()
        return self.cursor.fetchone()

    def fetch_all(self, sql):
        self.cursor.execute(sql)
        self.mysql.commit()
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.mysql.close()


if __name__ == '__main__':
    import datetime, time

    a = DoMysql().fetch_one(
        'SELECT Fmobile_no,Fverify_code FROM sms_db_07.t_mvcode_info_2 ORDER BY Fexpired_time ASC LIMIT 1')
    print(a['Fverify_code'])
    # c=a['Fsend_time']
    # # print(c)
    # b=a['Fexpired_time']
    # print(b)
    # # print(int(str(b)[-5:-3])-int(str(c)[-5:-3]))
    # # print(int(str(c)[-5:-3]))
    #
    # f=datetime.datetime.now()
    # print(f)
    #
    # if f<b:
    #     print(1)
    # else:
    #     print(2)
