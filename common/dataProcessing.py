#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time:2020/12/15 10:43
# @Author: wei.zhang
# @File : dataProcessing.py
# @Software: PyCharm
import os
from common.Log import Log
from common.DataAggregate import DataAggregate
from itertools import chain
from common.DataBaseOperatePool import DataBaseOperate
from datetime import datetime
from common.Config import Config
from common.dataConversion import DataConversion as conversion
from common.DBdataProcessing import AssemblyConfig, QuerySqliteData
from fileDir.fileDir import ENUMERATE_PATH


class dataProcessing(Config, QuerySqliteData):
    def __init__(self, configurationName=None, logName='dataProcessing', logLevel='DEBUG'):
        super(dataProcessing, self).__init__()
        AssemblyConfig()
        self.configurationName = configurationName
        self.sender_email = None
        self.password = None
        self.mysql_dict = None
        self.conf = None
        self.smtpHost = None
        self.L = Log(logName, logLevel).logger
        self.abs_path = os.path.dirname(os.path.abspath(__file__))
        self.initialize_parameter()
        self.db = DataBaseOperate()

    def initialize_parameter(self):
        """

        """
        if self.configurationName:
            self.conf = self.query_execution_conf(self.configurationName)
        else:
            self.L.debug("按照时间执行任务")
            self.conf = self.query_execution_conf(str(datetime.now().hour))
        if self.conf:
            env_conf = self.env_conf()
            self.sender_email = env_conf.get('EMAIL_SENDER')
            self.password = env_conf.get('EMAIL_PASSWD')
            self.mysql_dict = eval(env_conf.get('MYSQL_DICT'))
            self.smtpHost = self.conf.smtp_host
            self.assembly_receiver_data()
        else:
            # 传入的KEY没有在config文件中找到，或者执行时间与配置时间不匹配
            self.L.debug("没有可执行配置，请确认传入KEY或执行时间")
            raise Exception("没有可执行配置，请确认传入KEY或执行时间")

    def assembly_receiver_data(self):
        """
        获取收件人邮箱
        :return:
        """
        receobj = self.query_receiver_conf(self.conf)
        receiver = []
        for rece in receobj:
            receiver.append(rece.email)
        self.receiver = receiver

    def assembly_mapping_data(self, datas: list, lordId=None, viceId=None):
        """
        处理需要映射的数据
        :param datas: 查询结果数据
        :param lordId: 主表id
        :param viceId: 副表id
        :return:
        """
        mapping_list = self.query_mapping_conf(lordId, viceId)
        for mapping in mapping_list:
            mapping_file = mapping.mapping_file
            mapping_key = eval(mapping.mapping_key)
            enumerate_dict = Config().get_config(name=mapping_file, current_path=ENUMERATE_PATH)
            datas = conversion.replace_dict_value(replace_key=mapping_key,
                                                  keep_dict=datas,
                                                  enumerate_dict=enumerate_dict)
        return datas

    def _merge_data(self, conf: object, datas: list):
        """
        合并数据
        :return:
        """
        try:
            datas.remove(())
        except ValueError:
            pass
        try:
            datas.remove(None)
        except ValueError:
            pass
        if datas == [] or datas is None:
            return None
        if (conf.merge or conf.bus_vice_merge) and len(datas) > 1:
            # 判断是否达到合并条件
            merge_key = conf.merge_key if conf.merge else conf.bus_vice_merge_key
            if merge_key == 'None' or merge_key is None:
                # 合并单条类型的数据
                merge_data = list(chain.from_iterable(datas))
                result = {}
                [result.update(i) for i in merge_data]
                merge_data = result
            else:
                merge_data = DataAggregate().get_aggregate_result_copy(datas, merge_key)
            return merge_data
        else:
            return datas[0]

    def assembly_lord_data(self):
        """
        组装主数据
        :return:
        """
        lordData = {}
        bus_conf_all = self.query_busuness_conf(confobj=self.conf)
        for bus_conf in bus_conf_all:
            lord_conf_all = self.query_lord_conf(confObj=bus_conf)
            querydata = []
            for lord_conf in lord_conf_all:
                # 遍历拿到的主配置，并先处理副表数据
                datas = []
                vicedata = self.assembly_vice_data(lord_conf)
                sql_all = self.assembly_replace_data(lord_conf, vicedata)
                current_db_info = self.mysql_dict.get(lord_conf.db_name)
                self.db.creat_db_pool(current_db_info)
                for sql in sql_all:
                    _result = self.db.query_data(sql)
                    _result = self.assembly_mapping_data(_result, lord_conf.id)
                    datas.append(_result)
                if lord_conf.bus_vice_merge:
                    datas.append(vicedata[0])
                querydata.append(self._merge_data(lord_conf, datas))
                lordData[bus_conf.table_title] = self._merge_data(lord_conf, querydata)
        return lordData

    def assembly_replace_data(self, lordconf: object, vicedata: list):
        """
        替换SQL字段
        :param lordconf:
        :param vicedata:
        :param sqlList:
        :return:
        """
        sql_list = lordconf.busuness_sql.split(';')
        replace_conf_all = self.query_replace_data_conf(lordconf)
        sql_all = []
        if not replace_conf_all:
            for sql in sql_list:
                if sql != '':
                    sql = sql + ';'
                    sql_all.append(sql)
            return sql_all
        for sql in sql_list:
            for replace_conf in replace_conf_all:
                for vice in vicedata:
                    vice_original = DataAggregate.data_assemble(key=replace_conf.condition_value,
                                                                parameters_ld=vice)
                    if len(vice_original) > 1:
                        sql = sql.replace(replace_conf.replace_value, str(tuple(vice_original)))
                    elif len(vice_original) == 1:
                        sql = sql.replace(replace_conf.replace_value, str(vice_original[0]))
            if sql != '':
                sql = sql + ';'
                sql_all.append(sql)
        return sql_all

    def assembly_vice_data(self, lord_conf: object):
        """
        获取汇总表的条件数据
        :param lord_conf: 传数据库对象
        :return:
        """
        viceData = []
        vice_all = self.query_vice_conf(lordConfObj=lord_conf)
        # 获取数据表对象，进行遍历
        for vice_conf in vice_all:
            vice_sql = vice_conf.data_sql
            db_name = vice_conf.data_db_name
            self.db.creat_db_pool(self.mysql_dict.get(db_name))
            sql_list = vice_sql.split(';')
            datas = []
            for sql in sql_list:
                if sql == '':
                    continue
                datas.append(self.db.query_data(sql=sql + ';'))
            if len(datas) > 1:
                viceData.append(list(chain.from_iterable(datas)))
            elif len(datas) == 1:
                viceData.append(datas[0])
            if len(viceData) > 1:
                viceData = list(chain.from_iterable(viceData))
        return viceData
