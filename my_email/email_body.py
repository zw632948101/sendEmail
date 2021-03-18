#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time:2021/3/2 17:46
# @Author: wei.zhang
# @File : email_body.py
# @Software: PyCharm
from datetime import datetime
from fileDir.fileDir import ATTACHMENT
import pandas as pd
import re
from common.DBdataProcessing import QuerySqliteData

from my_email.sendEmail import sendEmail


class EmailBody(sendEmail):
    def __init__(self):
        super(EmailBody, self).__init__()
        self.result_data = ''
        self.conf = ''

    def assembly_data_send(self):
        """
        改方法功能：读取sql文件，1.将sql备注里的字典字符串转化为字典类型，并将sql注入到字典中
        :param confName:
        :return:
        """
        content = ''
        # 循环list获取数据库返回数据

        for result_key, result_value in self.result_data.items():
            content += f'<br /><h3>{result_key}</h3><br />'
            df = pd.DataFrame(result_value)
            df = df.fillna(value=0)
            table_sorting = QuerySqliteData().query_busuness_first(self.conf, result_key)
            table_field_sorting = table_sorting.table_field_sorting
            field_data_sorting = table_sorting.field_data_sorting
            if table_field_sorting or field_data_sorting:
                if eval(table_field_sorting):
                    try:
                        df = df[eval(table_field_sorting)]
                    except KeyError as e:
                        self.L.error(f'数据中字段与排序字段不一致：{e}')
                if field_data_sorting != 'None':
                    try:
                        df = df.sort_values(by=table_sorting.field_data_sorting, ascending=False)
                    except KeyError as e:
                        self.L.error(f'统计数据中没有：【{e}】 字段')
            content += df.to_html()
            filetime = datetime.strftime(datetime.now(), '%Y-%m-%d')
            df.to_excel(f"{ATTACHMENT}/{result_key}_{filetime}.xlsx")
        Subject = self.conf.email_title
        # 调用发送邮件方法
        param_rep = {r'0\.0</td>': '0</td>', '<td>0</td>': '<td>无</td>',
                     '<td>NaN</td>': '<td></td>',
                     r'\.0</td>': '</td>'}
        pattern = re.compile("|".join(param_rep.keys()))
        # content = pattern.sub(lambda m: param_rep[re.escape(m.group(0))], content)
        for k, v in param_rep.items():
            content.replace(k, v)
        self.flower_send_message(
            content=content,
            Subject=f"{datetime.strftime(datetime.now(), '%Y-%m-%d')} {Subject}")
