#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
__author__: wei.zhang
 @FILE     : flowerSendEmail.py
 @Time     : 2020/6/5 16:12
 @Software : PyCharm
"""
from Log import Log
from sendEmail import sendEmail
from DataBaseOperatePool import DataBaseOperate
import pandas as pd
import numpy as np
from DataAggregate import DataAggregate


class FlowerSendEmail(sendEmail):
    def __init__(self):
        super(FlowerSendEmail, self).__init__()
        self.L = Log("FlowerSendEmail", 'DEBUG').logger
        self.db = DataBaseOperate()
        self.db.creat_db_pool()

    def __del__(self):
        self.db.close_db_pool()

    def assembly_data_send(self):
        # 初始化变量
        flowersql = open('flowerSQL.sql', 'r', encoding='UTF-8').read()
        flowersql_list = flowersql.rsplit(';')
        content = ''
        Subject = ''
        sql_set = []
        keylist = []
        sql = []
        key_dict = {}
        lable_dict = {}
        names = locals()
        # 将sql加入字典中
        for sqlinfo in flowersql_list:
            sqllist = sqlinfo.rsplit('/')
            if sqlinfo != '':
                remak_dict = eval(sqllist[1].replace('*', '').replace('\n', ''))
                # if remak_dict.get('combine'):
                remak_dict['sql'] = sqllist[2] + ";"
                sql_set.append(remak_dict)
                keylist.append(remak_dict.get('combine_label'))
            else:
                pass
        # 获取重复key以及每个重复key的次数
        repetition_key_dict = dict(zip(*np.unique(keylist, return_counts=True)))
        repetition_key = list(repetition_key_dict.keys())
        valuation_repetition_key_dict = dict(zip(*np.unique(keylist, return_counts=True)))
        # 删除字典中小于2的key
        for key in valuation_repetition_key_dict.keys():
            if repetition_key_dict.get(key) < 2:
                del repetition_key_dict[key]
                repetition_key.remove(key)
        # 循环list获取数据库返回数据
        for i in sql_set:
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
            queryData = DataAggregate().get_aggregate_result_copy(datalist, key=key_dict.get(i))
            df = pd.DataFrame(queryData)
            content += df.to_html()
        # 调用发送邮件方法
        self.flower_send_message(content=content, Subject=Subject)


if __name__ == '__main__':
    f = FlowerSendEmail()
    f.assembly_data_send()