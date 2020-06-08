#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
__author__: wei.zhang
 @FILE     : flowerSendEmail.py
 @Time     : 2020/6/5 16:12
 @Software : PyCharm
"""
from common.Log import Log
from my_email.sendEmail import sendEmail
import pandas as pd
import numpy as np
from common.DataAggregate import DataAggregate
from itertools import chain


class FlowerSendEmail(sendEmail):
    def __init__(self):
        super(FlowerSendEmail, self).__init__()
        self.L = Log("FlowerSendEmail", 'DEBUG').logger

    def __del__(self):
        self.db.close_db_pool()

    def read_sql_file(self, filename):
        """
        改方法功能：读取sql文件，1.将sql备注里的字典字符串转化为字典类型，并将sql注入到字典中
        :param filename: 相对路径
        :return: sql_set和keylist
        """
        self.L.debug("执行sql文件 %s 组装sql字典" % filename)
        flowersql = open(filename, 'r', encoding='UTF-8').read()
        flowersql_list = flowersql.rsplit(';')
        sql_dict = []
        keylist = []
        for sqlinfo in flowersql_list:
            sqllist = sqlinfo.rsplit('/')
            if sqlinfo != '':
                remak_dict = eval(sqllist[1].replace('*', '').replace('\n', ''))
                remak_dict['sql'] = sqllist[2] + ";"
                sql_dict.append(remak_dict)
                keylist.append(remak_dict.get('combine_label'))
            else:
                pass
        return sql_dict, keylist

    def repetition_key_number(self, keylist):
        """
        计算list中重复值次数生成字典
        :param keylist: list
        :return: 返回重复值和次数字典，返回重复大于等于2次的值和次数字典，返回重复值大于等于2次的值
        """
        repetition_key_dict = dict(zip(*np.unique(keylist, return_counts=True)))
        repetition_key = list(repetition_key_dict.keys())
        valuation_repetition_key_dict = dict(zip(*np.unique(keylist, return_counts=True)))
        # 删除字典中小于2的key
        for key in valuation_repetition_key_dict.keys():
            if repetition_key_dict.get(key) < 2:
                del repetition_key_dict[key]
                repetition_key.remove(key)
        return repetition_key_dict, valuation_repetition_key_dict, repetition_key

    def assembly_data_send(self, filename):
        """
        改方法功能：读取sql文件，1.将sql备注里的字典字符串转化为字典类型，并将sql注入到字典中
        :param filename:
        :return:
        """
        # 初始化变量
        content = ''
        Subject = ''
        sql = []
        key_dict = {}
        lable_dict = {}
        names = locals()
        # 将sql加入字典中
        sql_dict, keylist = self.read_sql_file(filename=filename)
        if not sql_dict:
            self.L.error("文件是空的！")
            return
            # 获取重复key以及每个重复key的次数
        repetition_key_dict, valuation_repetition_key_dict, repetition_key = self.repetition_key_number(keylist)
        # 循环list获取数据库返回数据
        for i in sql_dict:
            # 判断key是否为重复key，如果为重复key时进行命名空间动态生成变量进行赋值
            if i.get('combine_label') in repetition_key:
                for k in repetition_key:
                    if i.get('combine_label') == k:
                        num = valuation_repetition_key_dict.get(k)
                        names[k + str(num - 1)] = self.db.query_data(i.get('sql'))
                        key_dict[k] = i.get('combine_key')
                        valuation_repetition_key_dict[k] = num - 1
                        lable_dict[k] = i.get('statement_title')
                        Subject = i.get('email_title')
            else:  # 如果key不重复时，使用pandas生成HTML格式数据
                content += '<br /><h3>%s</h3><br />' % i.get('statement_title')
                queryData = self.db.query_data(i.get('sql'))
                df = pd.DataFrame(queryData)
                content += df.to_html()
                Subject = i.get('email_title')
        # 对重复key的数据，先做数据合并，在使用pandas生成HTML格式数据
        for i in repetition_key:
            content += '<br /><h3>%s</h3><br />' % lable_dict.get(i)
            datalist = []
            for k in range(repetition_key_dict.get(i)):
                datalist.append(names.get(i + str(k)))
            if key_dict.get(i):
                queryData = DataAggregate().get_aggregate_result_copy(datalist, key=key_dict.get(i))
            else:
                queryData = list(chain.from_iterable(datalist))
                result = {}
                [result.update(i) for i in queryData]
                queryData = [result]
            df = pd.DataFrame(queryData)
            content += df.to_html()
        # 调用发送邮件方法
        self.flower_send_message(content=content, Subject=Subject)

    def read_files(self):
        import os
        for root, dirs, files in os.walk('sql/'):
            for file in files:
                if os.path.splitext(file)[1] == '.sql':
                    self.assembly_data_send(filename=os.path.join(root, file))


if __name__ == '__main__':
    f = FlowerSendEmail()
    f.read_files()
