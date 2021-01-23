#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
__author__: wei.zhang
 @FILE     : flowerSendEmail.py
 @Time     : 2020/6/5 16:12
 @Software : PyCharm
"""
import os, sys
from my_email.sendEmail import sendEmail
import pandas as pd
from datetime import datetime
from common.dataProcessing import dataProcessing
from common.fileOperating import FileOperating


class SqlStatementOverrun(Exception):
    def __init__(self):
        pass

    def __str__(self):
        print("SQL数量超限，一个文件只能有一个SQL")


class FlowerSendEmail(dataProcessing, sendEmail, FileOperating):
    def __init__(self, configurationName=None, logName='FlowerSendEmail'):
        self.configurationName = configurationName
        self.logName = logName
        super(FlowerSendEmail, self).__init__(configurationName=configurationName, logName=logName)
        self.abs_path = os.path.dirname(os.path.abspath(__file__))
        self.read_files()

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
            self.L.info("执行SQL：" + i.get('statement_title'))
            queryData = self.assembly_lord_data(sql_dict=i)
            if i.get("DBstatus") and queryData:
                queryData = self.assembly_vice_data(sql_dict=i, queryData=queryData)
            content += '<br /><h3>%s</h3><br />' % i.get('statement_title')
            df = pd.DataFrame(queryData)
            df = df.fillna(value="")
            if i.get('statement_title') == "每日采集蜂友统计":
                order = ['采集人', '采集日期', '采集人电话', '今日采集蜂友数', '今日采集蜂场数', '今日采蜂友场登录数',
                         '今日采集蜂场登录数', '开始采集时间', '结束采集时间', '推广蜂友天气设定人数', '推广蜂友发布蜂友互助的数量_人',
                         '推广蜂友发布蜂友互助的数量_条数', '1月20日后采集蜂友数', '1月20日后采集蜂场数']
                df = df.sort_values(by='今日采集蜂友数', ascending=False)
                df = df[order]
            content += df.to_html()
            df.to_excel(
                self.abs_path + '/attachment/' + i.get('statement_title') + datetime.strftime(
                    datetime.now(), '%Y-%m-%d') + '.xlsx')
            Subject = i.get('email_title')
        # 调用发送邮件方法
        self.flower_send_message(
            content=content.replace('0.0</td>', '0</td>').replace('<td>NaN</td>',
                                                                  '<td></td>').replace('.0</td>',
                                                                                       '</td>'),
            Subject="[%s] %s" % (datetime.strftime(datetime.now(), '%Y-%m-%d'), Subject))

    def read_files(self):
        for i in self.files:
            self.assembly_data_send(self.abs_path + '/sql/' + i)


if __name__ == '__main__':
    try:
        if sys.argv[1] != '':  # 线上使用
            _cf_key = sys.argv[1]
        else:
            _cf_key = None
    except IndexError as e:
        _cf_key = 'collectionFriendSwarmInfoStististics'
    f = FlowerSendEmail(_cf_key)
