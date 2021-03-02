#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
__author__: wei.zhang
 @FILE     : flowerSendEmail.py
 @Time     : 2020/6/5 16:12
 @Software : PyCharm
"""
import sys
from my_email.sendEmail import sendEmail
import pandas as pd
from datetime import datetime
from common.dataProcessing import dataProcessing
from common.fileOperating import FileOperating
from fileDir.fileDir import ATTACHMENT


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
        self.assembly_data_send()

    def assembly_data_send(self):
        """
        改方法功能：读取sql文件，1.将sql备注里的字典字符串转化为字典类型，并将sql注入到字典中
        :param confName:
        :return:
        """
        # 初始化变量
        self.del_file()

        content = ''
        result_data = self.assembly_lord_data()
        # 循环list获取数据库返回数据
        for result_key, result_value in result_data.items():
            content += f'<br /><h3>{result_key}</h3><br />'
            df = pd.DataFrame(result_value)
            df = df.fillna(value=0)
            if result_key == "每日采集蜂友统计":
                order = ['采集人', '采集日期', '采集人电话', '今日采集蜂友数', '今日采集蜂场数', '今日采蜂友场登录数',
                         '今日采集蜂场登录数', '开始采集时间', '结束采集时间', '推广蜂友天气设定人数', '推广蜂友发布蜂友互助的数量_人',
                         '推广蜂友发布蜂友互助的数量_条数', '1月20日后采集蜂友数', '1月20日后采集蜂场数']
                df = df.sort_values(by='今日采集蜂友数', ascending=False)
                df = df[order]
            content += df.to_html()
            filetime = datetime.strftime(datetime.now(), '%Y-%m-%d')
            df.to_excel(f"{ATTACHMENT}/{result_key}_{filetime}.xlsx")
        Subject = self.conf.email_title
        # 调用发送邮件方法
        self.flower_send_message(
            content=content.replace('0.0</td>', '0</td>').replace('<td>NaN</td>',
                                                                  '<td></td>').replace('.0</td>',
                                                                                       '</td>'),
            Subject="[%s] %s" % (datetime.strftime(datetime.now(), '%Y-%m-%d'), Subject))


if __name__ == '__main__':
    try:
        if sys.argv[1] != '':  # 线上使用
            _cf_key = sys.argv[1]
        else:
            _cf_key = None
    except IndexError as e:
        _cf_key = None
    f = FlowerSendEmail(_cf_key)
