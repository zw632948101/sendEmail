#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time:2020/12/15 10:43
# @Author: wei.zhang
# @File : dataProcessing.py
# @Software: PyCharm

import os
import shutil
from common.Log import Log
import pandas as pd
from common.DataAggregate import DataAggregate
from itertools import chain
from common.DataBaseOperatePool import DataBaseOperate
from datetime import datetime
from common.Config import Config


class SqlStatementOverrun(Exception):
    def __init__(self):
        pass

    def __str__(self):
        print("SQL数量超限，一个文件只能有一个SQL")


class dataProcessing(Config):
    def __init__(self, configurationName=None, logName='dataProcessing', logLevel='DEBUG'):
        super(dataProcessing, self).__init__(name='config')
        self.configurationName = configurationName
        self.L = Log(logName, logLevel).logger
        self.abs_path = os.path.dirname(os.path.abspath(__file__))
        self.initialize_parameter()
        self.db = DataBaseOperate()
        self.db.creat_db_pool(self.config)

    def initialize_parameter(self):
        """
        sys.argv 直接取下标会抛下标越界异常
        """
        if self.configurationName:
            cf_key = self.data.get(self.configurationName)
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
                # 检查是否有跨库查询，将需要跨库的SQL注入到字典中
                if remak_dict.get('DBstatus'):
                    db_list = []
                    for dbl in remak_dict.get('DBlist'):
                        dblsql = open(self.abs_path + '/sql/substatements/' + dbl.get('sqlfile'),
                                      'r', encoding='UTF-8').read()
                        dblsql = [i + ';' for i in dblsql.rsplit(';')][:-1]
                        if len(dblsql) > 1:
                            raise SqlStatementOverrun
                        dbl['sql'] = dblsql[0]
                        db_list.append(dbl)
                    remak_dict['DBlist'] = db_list
                sql_list.append(remak_dict)

        return sql_list

    def assembly_lord_data(self, sql_dict):
        """
        组装主数据
        :param sql_dict:
        :return:
        """
        if sql_dict.get('DBname'):
            mysqldict = eval(self.config.get('MYSQL_DICT'))
            self.db.creat_db_pool(mysqldict.get(sql_dict.get('DBname')))
        queryData = []
        if len(sql_dict.get('sql')) >= 2:
            datalist = []
            if sql_dict.get('combine'):  # sql列表长度大于2，判断combine为True，如果为true合并sql查询结果
                if sql_dict.get('combine_key'):  # 判断有么有合并key，有使用key合并数据
                    for k in range(len(sql_dict.get('sql'))):
                        datalist.append(self.db.query_data(sql_dict.get('sql')[k]))
                    queryData = DataAggregate().get_aggregate_result_copy(datalist,
                                                                          key=sql_dict.get(
                                                                              'combine_key'))
                else:  # 没有combine_key或为空，直接合并
                    for k in range(len(sql_dict.get('sql'))):
                        datalist.append(self.db.query_data(sql_dict.get('sql')[k]))
                    queryData = list(chain.from_iterable(datalist))
                    result = {}
                    [result.update(i) for i in queryData]
                    queryData = [result]
            else:  # 如果combine为False，不合并sql查询结果
                for k in range(len(sql_dict.get('sql'))):
                    queryData.append(self.db.query_data(sql_dict.get('sql')[k]))
        else:  # 字典内sql列表长度等于1，查询结果直接处理
            queryData = self.db.query_data(sql_dict.get('sql')[0])
        self.db.close_db_pool()
        return queryData

    def assembly_vice_data(self, sql_dict, queryData):
        """
        组装数据
        :param sql_dict:
        :param queryData:
        :return:
        """

        def replacekey(sql, keys):
            """
            替换SQL中关键字
            :param sql:
            :param keys:
            :return:
            """
            for k in keys:
                keyl = []
                if isinstance(queryData[0], list):
                    for parameters in queryData:
                        keyl = DataAggregate.data_assemble(key=k.get("Value"),
                                                           parameters_ld=parameters)
                        if keyl != []:
                            break
                else:
                    keyl = DataAggregate.data_assemble(key=k.get("Value"), parameters_ld=queryData)
                if len(keyl) > 1:
                    sql = sql.replace(k.get("replace"), str(tuple(keyl)))
                else:
                    sql = sql.replace(k.get("replace"), "(%s)" % keyl[0])
            return sql

        viceData = []
        datalist = []
        if sql_dict.get('LORD_VICE_MERGE'):  # 判断主表和副表是否需要合并，为true时加入主表数据
            viceData.append(queryData)
        for dbc in sql_dict.get('DBlist'):  # 循环遍历需要查询的副表SQL列表
            db_key = dbc.get('db_key')
            mysqldict = eval(self.config.get('MYSQL_DICT'))
            self.db.creat_db_pool(mysqldict.get(dbc.get('DBname')))
            sql = dbc.get('sql')
            sql = replacekey(sql, db_key)
            if sql_dict.get('LORD_VICE_MERGE'):
                viceData.append(self.db.query_data(sql=sql))
                if dbc.get('MERGE_KEY'):  # 判断是否有合并字段，有值时根据合并字段将副表合并至主表
                    datalist = DataAggregate().Master_schedule_aggregate(viceData,
                                                                         key=dbc.get('MERGE_KEY'))
                    viceData = [datalist]
                if not dbc.get('MERGE_KEY'):  # 没有合并字段时直接进行合并（注意合并后查看数据不清晰）
                    vd = list(chain.from_iterable(viceData))
                    result = {}
                    [result.update(i) for i in vd]
                    datalist = [result]
                    viceData = [datalist]
            if not sql_dict.get('LORD_VICE_MERGE') and sql_dict.get('VICE_MERGE'):
                # 主表不需要合并，副表之间合并
                dbinfo = self.db.query_data(sql=sql)
                if dbinfo != []:
                    viceData.append(dbinfo)
                # 在多张副表时才执行合并，如果只有一张副表就直接处理
                if len(viceData) >= 2 and dbc.get('MERGE_KEY'):
                    datalist = DataAggregate().get_aggregate_result_copy(viceData,
                                                                         key=dbc.get('MERGE_KEY'))
                    viceData = [datalist]
                elif len(viceData) >= 2 and not dbc.get('MERGE_KEY'):
                    vd = list(chain.from_iterable(viceData))
                    result = {}
                    vd = [result.update(i) for i in vd]
                    datalist = vd
                    viceData = [datalist]
        self.db.close_db_pool()
        return datalist
