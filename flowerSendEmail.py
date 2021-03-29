#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
__author__: wei.zhang
 @FILE     : flowerSendEmail.py
 @Time     : 2020/6/5 16:12
 @Software : PyCharm
"""
import sys
from my_email.email_body import EmailBody
from common.dataProcessing import dataProcessing
from common.fileOperating import FileOperating


class SqlStatementOverrun(Exception):
    def __init__(self):
        pass

    def __str__(self):
        print("SQL数量超限，一个文件只能有一个SQL")


class FlowerSendEmail(dataProcessing, FileOperating, EmailBody):
    def __init__(self, configurationName=None, logName='FlowerSendEmail'):
        super(FlowerSendEmail, self).__init__(configurationName=configurationName, logName=logName)
        self.configurationName = configurationName
        self.logName = logName
        self.del_file()
        self.result_data = self.assembly_lord_data()
        self.assembly_data_send()


if __name__ == '__main__':
    try:
        if sys.argv[1] != '':  # 线上使用
            _cf_key = sys.argv[1]
        else:
            _cf_key = None
    except IndexError as e:
        _cf_key = None
    f = FlowerSendEmail(_cf_key)
