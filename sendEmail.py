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
from Config import Config
from Log import Log
from sql import sendEmailSQL
import pandas as pd


class sendEmail(sendEmailSQL):
    def __init__(self):
        super(sendEmail, self).__init__()
        self.L = Log("snedEmail", 'DEBUG').logger
        emailinfo = Config('config').data.get('email')
        self.email = emailinfo.get('sender')
        self.password = emailinfo.get('password')
        self.smtpHost = emailinfo.get('smtpHost')
        self.receiver = emailinfo.get('receiver')

    def send_message(self, datalist, Subject):
        try:
            # 发送邮件结果
            self.L.info("通过Email发送报表")
            df = pd.DataFrame(datalist)
            msg = MIMEText(df.to_html(), 'txt', 'utf-8')
            msg['Subject'] = Subject
            msg['From'] = self.email
            msg['To'] = ",".join(self.receiver)
            smtp_server = smtplib.SMTP_SSL(self.smtpHost, 465)
            smtp_server.login(self.email, self.password)
            smtp_server.sendmail(self.email, self.receiver, msg.as_string())
            smtp_server.quit()
            self.L.info("发送邮件结束")
        finally:
            pass

    def test_dict(self):
        datainfo = self.offline_promotion_personnel_statistics()
        self.send_message(datalist=datainfo, Subject="测试报表")


if __name__ == '__main__':
    se = sendEmail()
    se.test_dict()
