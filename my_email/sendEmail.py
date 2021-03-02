#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
__author__: wei.zhang
 @FILE     : sendEmail.py
 @Time     : 2020/6/4 14:42
 @Software : PyCharm
"""
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from common.Log import Log
from email.utils import formataddr
from email.header import Header
import os
from fileDir.fileDir import ATTACHMENT


class sendEmail():
    def __init__(self):
        super(sendEmail, self).__init__()
        self.L = Log("snedEmail", 'DEBUG').logger
        self.sender_email = 'EMAIL_SENDER'
        self.password = 'EMAIL_PASSWD'
        self.smtpHost = 'smtpHost'
        self.receiver = 'receiver'

    def flower_send_message(self, content, Subject):
        try:
            # 发送邮件结果

            self.L.info("通过Email发送报表")
            msg = MIMEMultipart()
            for root, dirs, files in os.walk(ATTACHMENT):
                for file in files:
                    file_name = os.path.join(root, file)
                    with open(file_name, 'rb') as f:
                        mime = MIMEBase('1', 'xlsx', filename=file)
                        mime.add_header('Content-Disposition', 'attachment', filename=file)
                        mime.add_header('Content-ID', '<0>')
                        mime.add_header('X-Attachment-Id', '0')
                        mime.set_payload(f.read())
                        encoders.encode_base64(mime)
                        msg.attach(mime)
            msg.attach(MIMEText(content, 'html', 'utf-8'))
            msg['Subject'] = Subject
            msg['From'] = formataddr((Header("追花族", 'utf-8').encode(), self.sender_email))
            msg['To'] = ",".join(self.receiver)
            smtp_server = smtplib.SMTP_SSL(self.smtpHost, 465)
            smtp_server.login(self.sender_email, self.password)
            smtp_server.sendmail(self.sender_email, self.receiver, msg.as_string())
            smtp_server.quit()
            self.L.info("发送邮件结束")
        finally:
            pass
