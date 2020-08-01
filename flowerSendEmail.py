#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
__author__: wei.zhang
 @FILE     : flowerSendEmail.py
 @Time     : 2020/6/5 16:12
 @Software : PyCharm
"""
import os
import shutil
import sys
from common.Log import Log
from my_email.sendEmail import sendEmail
import pandas as pd
import numpy as np
from common.DataAggregate import DataAggregate
from itertools import chain
from common.DataBaseOperatePool import DataBaseOperate
from datetime import datetime
from common.Config import Config


class FlowerSendEmail(Config, sendEmail):
    def __init__(self):
        super(FlowerSendEmail, self).__init__(name='config')
        self.L = Log("FlowerSendEmail", 'DEBUG').logger
        self.initialize_parameter()
        self.db = DataBaseOperate()
        self.db.creat_db_pool(self.config)
        self.read_files()
        self.abs_path = os.path.dirname(os.path.abspath(__file__))

    def initialize_parameter(self):
        """
        sys.argv 直接取下标会抛下标越界异常
        """
        if sys.argv[1] != '':
            self.L.debug("按照传入配置执行任务")
            cf_key = self.data.get(sys.argv[1])
        else:
            self.L.debug("按照时间执行任务")
            cf_key = self.data.get(datetime.now().hour)
        if cf_key:
            self.files = cf_key.get('sql_file')
            self.L.debug(self.files)
            self.execute_time = cf_key.get('execute_time')
            self.config = self.get_yaml_dict(cf_key)
            self.email = self.config.get('EMAIL_SENDER')
            self.password = self.config.get('EMAIL_PASSWD')
            self.smtpHost = self.config.get('smtpHost')
            self.receiver = self.config.get('receiver')
        else:
            # 传入的KEY没有在config文件中找到，或者执行时间与配置时间不匹配
            self.L.debug("没有可执行配置，请确认传入KEY或执行时间")
            raise Exception("没有可执行配置，请确认传入KEY或执行时间")

    def __del__(self):
        self.db.close_db_pool()

    def del_file(self, filepath):
        """
        删除某一目录下的所有文件或文件夹
        :param filepath: 路径
        :return:
        """
        del_list = os.listdir(filepath)
        for f in del_list:
            file_path = os.path.join(filepath, f)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    def read_sql_file(self, filename):
        """
        改方法功能：读取sql文件，1.将sql备注里的字典字符串转化为字典类型，并将sql注入到字典中
        :param filename: 相对路径
        :return: sql_set和keylist
        """
        self.L.debug("执行sql文件 %s 组装sql字典" % filename)
        flowersql = open(filename, 'r', encoding='UTF-8').read()
        flowersql = flowersql.replace('\n{', '{')
        sql_list = []
        for sqlinfo in flowersql.rsplit('/*'):
            if sqlinfo:
                remak_dict, sqlstr = sqlinfo.rsplit('*/')
                remak_dict = eval(remak_dict)
                remak_dict['sql'] = [i + ';' for i in sqlstr.rsplit(';')][:-1]
                sql_list.append(remak_dict)
        return sql_list

    def assembly_data_send(self, filename):
        """
        改方法功能：读取sql文件，1.将sql备注里的字典字符串转化为字典类型，并将sql注入到字典中
        :param filename:
        :return:
        """
        # 初始化变量
        self.del_file(self.abs_path + '/attachment/')
        content = ''
        Subject = ''
        # 将sql加入字典中
        sql_dict = self.read_sql_file(filename=filename)
        if not sql_dict:
            self.L.error("文件是空的！")
            return
        # 循环list获取数据库返回数据
        for i in sql_dict:
            # 判断字典内sql列表长度是否大于2
            queryData = []
            if len(i.get('sql')) >= 2:
                datalist = []
                if i.get('combine'):  # sql列表长度大于2，判断combine为True，如果为true合并sql查询结果
                    if i.get('combine_key'):  # 判断有么有合并key，有使用key合并数据
                        for k in range(len(i.get('sql'))):
                            datalist.append(self.db.query_data(i.get('sql')[k]))
                        queryData = DataAggregate().get_aggregate_result_copy(datalist, key=i.get('combine_key'))
                    else:  # 没有combine_key或为空，直接合并
                        for k in range(len(i.get('sql'))):
                            datalist.append(self.db.query_data(i.get('sql')[k]))
                        queryData = list(chain.from_iterable(datalist))
                        result = {}
                        [result.update(i) for i in queryData]
                        queryData = [result]
                else:  # 如果combine为False，不合并sql查询结果
                    for k in range(len(i.get('sql'))):
                        queryData.append(self.db.query_data(i.get('sql')[k]))
            else:  # 字典内sql列表长度等于1，查询结果直接处理
                queryData = self.db.query_data(i.get('sql')[0])
            content += '<br /><h3>%s</h3><br />' % i.get('statement_title')
            df = pd.DataFrame(queryData)
            df = df.fillna(value=0)
            content += df.to_html()
            df.to_excel(
                self.abs_path + '/attachment/' + i.get('statement_title') + datetime.strftime(datetime.now(), '%Y-%m-%d') + '.xlsx')
            Subject = i.get('email_title')
        # 调用发送邮件方法
        self.flower_send_message(
            content=content.replace('0.0</td>', '0</td>').replace('<td>NaN</td>', '<td>0</td>').replace('.0</td>',
                                                                                                        '</td>'),
            Subject="[%s] %s" % (datetime.strftime(datetime.now(), '%Y-%m-%d'), Subject))

    def read_files(self):
        execute_sql = False

        for root, dirs, files in os.walk(self.abs_path + '/sql/'):
            for file in files:
                if file in self.files:
                    execute_sql = True
                    self.assembly_data_send(filename=os.path.join(root, file))
        if not execute_sql:
            self.L.info('没有找到要执行的sql')


if __name__ == '__main__':
    f = FlowerSendEmail()
