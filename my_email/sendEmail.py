#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
__author__: wei.zhang
 @FILE     : sendEmail.py
 @Time     : 2020/6/4 14:42
 @Software : PyCharm
"""
import smtplib
from email.mime.text import MIMEText
from common.Config import Config
from common.Log import Log
import pandas as pd
from email.utils import formataddr
from email.header import Header


class sendEmail():
    def __init__(self):
        super(sendEmail, self).__init__()
        self.L = Log("snedEmail", 'DEBUG').logger
        emailinfo = Config.get_yaml_dict()
        self.email = emailinfo.get('sender')
        self.password = emailinfo.get('EMAIL_PASSWD')
        self.smtpHost = emailinfo.get('smtpHost')
        self.receiver = emailinfo.get('receiver')

    def send_message(self, datalist, Subject):
        try:
            # 发送邮件结果
            self.L.info("通过Email发送报表")
            df = pd.DataFrame(datalist)
            msg = MIMEText(df.to_html(), 'html', 'utf-8')
            msg['Subject'] = Subject
            msg['From'] = formataddr((Header("追花采集统计", 'utf-8').encode(), self.email))
            msg['To'] = ",".join(self.receiver)
            smtp_server = smtplib.SMTP_SSL(self.smtpHost, 465)
            smtp_server.login(self.email, self.password)
            smtp_server.sendmail(self.email, self.receiver, msg.as_string())
            smtp_server.quit()
            self.L.info("发送邮件结束")
        finally:
            pass

    def flower_send_message(self, content, Subject):
        try:
            # 发送邮件结果
            self.L.info("通过Email发送报表")
            msg = MIMEText(content, 'html', 'utf-8')
            msg['Subject'] = Subject
            msg['From'] = formataddr((Header("追花采集统计", 'utf-8').encode(), self.email))
            msg['To'] = ",".join(self.receiver)
            smtp_server = smtplib.SMTP_SSL(self.smtpHost, 465)
            smtp_server.login(self.email, self.password)
            smtp_server.sendmail(self.email, self.receiver, msg.as_string())
            smtp_server.quit()
            self.L.info("发送邮件结束")
        finally:
            pass

    # def send_flowers_collection_statistics(self):
    #     self.send_message(datalist=self.flowers_collection_statistics,
    #                       Subject="每日采集统计 [%s]" % datetime.strftime(datetime.now(), '%Y-%m-%d'))
    #
    #     self.send_message(datalist=self.flowers_statistics,
    #                       Subject="累计采集统计 [%s]" % datetime.strftime(datetime.now(), '%Y-%m-%d'))

# def query():
#     test = sendEmail()
#     test.send_flowers_collection_statistics()
#
#
# query()
