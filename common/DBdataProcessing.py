#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time:2020/11/23 09:55
# @Author: wei.zhang
# @File : DBdataProcessing.py
# @Software: PyCharm
from common.Config import Config
from fileDir.fileDir import CONFIG, SQL_CONFIG, LORD_SQL, VICE_SQL
from common.Log import Log
from model.dbEngine import DBEngine
from model.t_config import TConfig
from model.t_vice_data import ViceData
from model.t_replace_data import ReplaceData
from common.fileOperating import FileOperating
from model.t_receiver import Receiver
from model.t_sub_busuness import SubBusuness
from model.t_busuness import Busuness
from model.t_mapping import MappingConf
from sqlalchemy.sql import and_


class ConfigFileNoneError(Exception):
    def __init__(self, mer):
        self.mer = mer

    def __str__(self):
        print("没有可执行的SQL配置，请检查配置是否正确？")


class AssemblyConfig:
    """
    将配置写到数据库中存储
    """

    def __init__(self, loglevel="DEBUG"):
        """
        初始化配置参数
        :param configurationName:
        :param loglevel:
        """
        super(AssemblyConfig, self).__init__()
        self.L = Log(name=AssemblyConfig.__name__, level=loglevel).logger
        self._db_engine = DBEngine()
        self.configurationName = ''
        self.env_conf = {}
        self.version = False
        self.execution_c = {}
        self.sql_conf = {}
        self.initial_configuration()

    def initial_configuration(self):
        """
        初始化配置入口
        :return:
        """
        self.L.info("初始化配置开始。。。。。。。")
        all_c = Config().get_config(current_path=CONFIG, name='config')
        for configurationName in all_c:
            if configurationName == 'initialValue':
                continue
            self.read_config(all_c, configurationName)
            self.read_sql_conf()
            self.assert_conf_update()
        self.L.info("初始化配置结束。。。。。。。")

    def read_config(self, all_c, configurationName):
        """
        读取config配置
        :param configurationName:
        :return:
        """
        self.L.info("开始读取执行配置。。。。。。。")
        self.configurationName = configurationName
        if configurationName:
            self.L.info(f"使用传入执行配置:{configurationName}")
            self.execution_c = all_c.get(configurationName)
        if not self.execution_c:
            self.L.debug("没有可执行配置，请确认传入KEY或执行时间")
            raise Exception("没有可执行配置，请确认传入KEY或执行时间")
        self.env_conf = Config().get_yaml_dict(self.execution_c)
        self.L.info("读取执行配置结束。。。。。。。")

    def read_sql_conf(self):
        """
        读取SQL配置文件
        :param execution_conf:
        :return:
        """
        self.L.info("读取执行SQL配置.......")
        self.sql_conf = Config().get_config(current_path=SQL_CONFIG,
                                            name=self.execution_c.get('SQL_CONFIG'))
        if not self.sql_conf:
            self.L.debug('没有可执行的SQL配置，请检查配置是否正确？')
            raise ConfigFileNoneError(self.execution_c.get('SQL_CONFIG'))
        self.L.info("读取执行SQL配置结束.......")

    def assert_conf_update(self):
        """
        执行初始化配置写入数据库
        :return:
        """
        self.L.info(f"执行配置'{self.configurationName}'写入数据库......")
        session = self._db_engine.creat_session()
        tconfig = session.query(TConfig).filter(
            and_(TConfig.conifg_name == self.configurationName, TConfig.is_delete == 0)).first()
        if tconfig == [] or tconfig is None:
            # 如果配置在数据库为空，执行新增配置
            self._db_engine.close_session()
            self.write_conf()
            self.write_receiver()
            self.write_busuness_conf()
            self.write_lord_and_vice_conf()
        elif int(tconfig.conf_version) < int(self.sql_conf.get('CONF_VERSION')):
            # 如果已有配置，检查配置是否需要更新
            self.L.info(f'检测到已有配置：{self.configurationName}，进行更新')
            tconf = session.query(TConfig).filter(
                and_(TConfig.conifg_name == self.configurationName, TConfig.is_delete == 0)).first()
            tconf.email_title = self.sql_conf.get('EMAIL_TITLE')
            tconf.conf_version = str(self.sql_conf.get('CONF_VERSION'))
            tconf.table_title = str(self.sql_conf.get('TABLE_TITLE'))
            session.commit()
            self._db_engine.close_session()
            self.write_receiver()
            self.write_busuness_conf()
            self.write_lord_and_vice_conf()
        elif (tconfig != [] or tconfig is not None) and int(tconfig.conf_version) == int(
                self.sql_conf.get('CONF_VERSION')):
            self.L.info(f'检测到已有配置：{self.configurationName}，不需要更新')
            self._db_engine.close_session()
        self.L.info(f"执行配置'{self.configurationName}'写入数据库完成")

    def write_conf(self):
        """
        向数据库写执行配置
        :return:
        """
        session = self._db_engine.creat_session()
        self.L.info(f'进行新增配置：{self.configurationName}')
        addconfig = TConfig(conifg_name=self.configurationName,
                            email_title=self.sql_conf.get('EMAIL_TITLE'),
                            conf_version=str(self.sql_conf.get('CONF_VERSION')),
                            smtp_host=str(self.env_conf.get('SMTP_HOST')))
        session.add(addconfig)
        session.commit()
        self._db_engine.close_session()

    def write_busuness_conf(self):
        """
        写入业务配置
        :return:
        """
        session = self._db_engine.creat_session()
        tconfig = session.query(TConfig.id).filter(
            and_(TConfig.conifg_name == self.configurationName, TConfig.is_delete == 0)).first()
        self.L.info("写入业务配置")
        bus_all = session.query(Busuness.id).filter(
            and_(Busuness.cId == tconfig.id, Busuness.is_delete == 0)).all()
        for bus_data in bus_all:
            lord_all = session.query(SubBusuness.id).filter(
                and_(SubBusuness.b_id == bus_data.id, Busuness.is_delete == 0)).all()
            # 查询全部的配置信息，先删除已有的配置在添加
            self.L.info("查询全部的主副表配置信息，删除后重新添加。")
            for lord_a in lord_all:
                session.query(ReplaceData).filter(
                    and_(ReplaceData.l_id == lord_a.id, ReplaceData.is_delete == 0)).delete()
                session.query(ViceData).filter(
                    and_(ViceData.l_id == lord_a.id, ViceData.is_delete == 0)).delete()
                session.query(MappingConf).filter(
                    and_(MappingConf.l_id == lord_a.id, MappingConf.is_delete == 0)).delete()
            session.query(SubBusuness).filter(
                and_(SubBusuness.b_id == bus_data.id, SubBusuness.is_delete == 0)).delete()
        session.query(Busuness).filter(
            and_(Busuness.cId == tconfig.id, Busuness.is_delete == 0)).delete()
        for bus_conf in self.sql_conf.get('BUSUNESS'):
            if bus_conf.get('TABLE_FIELD_SORTING'):
                busunessconf = Busuness(cId=tconfig.id, table_title=bus_conf.get('TABLE_TITLE'),
                                        table_field_sorting=str(
                                            bus_conf.get('TABLE_FIELD_SORTING')),
                                        field_data_sorting=str(bus_conf.get('FIELD_DATA_SORTING')))
            else:
                busunessconf = Busuness(cId=tconfig.id, table_title=bus_conf.get('TABLE_TITLE'))
            session.add(busunessconf)
        session.commit()
        self._db_engine.close_session()

    def write_receiver(self):
        """
        写入邮箱
        :return:
        """
        self.L.info(f"将配置{self.configurationName}写入数据库。")
        receiver_list = self.env_conf.get('receiver')
        session = self._db_engine.creat_session()
        tconfig = session.query(TConfig.id).filter(
            and_(TConfig.conifg_name == self.configurationName, TConfig.is_delete == 0)).first()
        session.query(Receiver).filter(
            and_(Receiver.cId == tconfig.id, Receiver.is_delete == 0)).delete()
        for receiver in receiver_list:
            rece = Receiver(cId=tconfig.id, email=receiver)
            session.add(rece)
        session.commit()
        self._db_engine.close_session()

    def write_mapping_conf(self, mapping: list, lordId: int, viceId=None):
        """
        写入映射的值
        :param mapping:
        :param lordId:
        :param viceId:
        :return:
        """
        if mapping:
            session = self._db_engine.creat_session()
            for mg in mapping:
                mapping_key = str(mg.get('MAPPING_KEY'))
                mapping_file = mg.get('MAPPING_FILE')
                self.L.info(mg)
                self.L.info(f"添加映射配置........")
                if mapping_key is None or mapping_file is None or mapping_file == 'None' or mapping_key == 'None':
                    continue
                if viceId:
                    mapconf = MappingConf(mapping_key=mapping_key, mapping_file=mapping_file,
                                          l_id=lordId, v_id=viceId)
                else:
                    mapconf = MappingConf(mapping_key=mapping_key, mapping_file=mapping_file,
                                          l_id=lordId)
                session.add(mapconf)
            session.commit()
            self._db_engine.close_session()

    def _write_vice_conf(self, viceConf: list, lordId: int):
        """
        写入副表配置
        :param viceConf:
        :param lordId:
        :return:
        """
        session = self._db_engine.creat_session()
        for vice_c in viceConf:
            # 遍历副表配置
            data_db_name = vice_c.get('DATA_DB_NAME')
            data_name = vice_c.get('DATA_NAME')
            data_file = f"{VICE_SQL}/{vice_c.get('DATA_SQL_FILE')}"
            data_sql = FileOperating().read_file(data_file)
            self.L.info(vice_c)
            self.L.info(f"添加执行配置{self.configurationName}的副表SQL查询配置{data_sql}")
            vice = ViceData(data_db_name=data_db_name, l_id=lordId, data_sql=data_sql,
                            data_name=data_name)
            session.add(vice)
            session.commit()
            vice = session.query(ViceData).filter(
                and_(ViceData.l_id == lordId, ViceData.data_name == data_name,
                     ViceData.data_sql == data_sql)).first()
            self.write_mapping_conf(vice_c.get('DATA_MAPPING'), lordId, vice.id)
        self._db_engine.close_session()

    def write_replace_data_conf(self, replaceConf: dict, lordId: int):
        """
        写入变量替换操作配置
        :param replaceConf:
        :param lordId:
        :return:
        """
        session = self._db_engine.creat_session()
        for replace_data in replaceConf:
            # 变量替换操作配置
            replace_value = replace_data.get('REPLACE_VALUE')
            condition_value = replace_data.get('CONDITION_VALUE')
            self.L.info(
                f"添加执行配置{self.configurationName}的替换值{replace_value}和原始值{condition_value}")
            replace_d = ReplaceData(l_id=lordId, replace_value=replace_value,
                                    condition_value=condition_value)
            session.add(replace_d)
            session.commit()
        self._db_engine.close_session()

    def write_lord_and_vice_conf(self):
        """
        写入主表配置和副表配置
        :return:
        """
        session = self._db_engine.creat_session()
        tconfig = session.query(TConfig.id).filter(
            and_(TConfig.conifg_name == self.configurationName, TConfig.is_delete == 0)).first()
        for bus_conf in self.sql_conf.get('BUSUNESS'):
            bus_data = session.query(Busuness).filter(
                and_(Busuness.cId == tconfig.id, Busuness.is_delete == 0,
                     Busuness.table_title == bus_conf.get('TABLE_TITLE'))).first()
            for lord_c in bus_conf.get('SUB_BUSUNESS'):
                # 变量主表配置
                merge = lord_c.get('MERGE')
                merge_key = lord_c.get('MERGE_KEY')
                db_name = lord_c.get('DB_NAME')
                busuness_name = lord_c.get('BUSUNESS_NAME')
                bus_vice_merge = lord_c.get('BUSUNESS_VICE_MERGE')
                bus_vice_merge_key = lord_c.get('BUSUNESS_VICE_MERGE_KEY')
                lord_file = f"{LORD_SQL}/{lord_c.get('BUSUNESS_SQL_FILE')}"
                sql = FileOperating().read_file(lord_file)
                self.L.info(lord_c)
                self.L.info(f"添加执行配置{self.configurationName}的主表SQL查询配置{busuness_name}")
                if bus_vice_merge:
                    load = SubBusuness(b_id=bus_data.id, merge_key=merge_key,
                                       merge=merge, db_name=db_name, busuness_sql=sql,
                                       busuness_name=busuness_name,
                                       bus_vice_merge_key=bus_vice_merge_key,
                                       bus_vice_merge=bus_vice_merge)
                else:
                    load = SubBusuness(b_id=bus_data.id, merge_key=merge_key,
                                       merge=merge, db_name=db_name, busuness_sql=sql,
                                       busuness_name=busuness_name)
                session.add(load)
                session.commit()
                busuness = session.query(SubBusuness.id).filter(
                    and_(SubBusuness.b_id == bus_data.id, SubBusuness.busuness_sql == sql,
                         SubBusuness.busuness_name == busuness_name,
                         SubBusuness.is_delete == 0)).first()
                if lord_c.get('BUSUNESS_MAPPING'):
                    self.write_mapping_conf(lord_c.get('BUSUNESS_MAPPING'), busuness.id)
                else:
                    self.L.info('当前配置映射配置数据')
                if lord_c.get('VICE_DATA'):
                    self._write_vice_conf(lord_c.get('VICE_DATA'), busuness.id)
                else:
                    self.L.info('当前配置没有数据表的配置数据')
                if lord_c.get('REPLACE_KEY'):
                    self.write_replace_data_conf(lord_c.get('REPLACE_KEY'), busuness.id)
                else:
                    self.L.info('当前配置替换字段配置数据')
            self._db_engine.close_session()


class QuerySqliteData:
    def __init__(self, loglevel='DEBUG'):
        super(QuerySqliteData, self).__init__()
        # self.L = Log(name=AssemblyConfig.__name__, level=loglevel).logger
        self._db_engine = DBEngine()

    def query_execution_conf(self, executionConfName):
        """
        获取执行配置数据
        :param executionConfName:
        :return:
        """
        session = self._db_engine.creat_session()
        e_conf = session.query(TConfig).filter(
            and_(TConfig.conifg_name == executionConfName, TConfig.is_delete == 0)).first()
        self._db_engine.close_session()
        return e_conf

    def query_lord_conf(self, confObj: object):
        """
        需要传一个数据库对象
        :param confObj:
        :return:
        """
        session = self._db_engine.creat_session()
        l_conf = session.query(SubBusuness).filter(
            and_(SubBusuness.b_id == confObj.id, SubBusuness.is_delete == 0)).all()
        self._db_engine.close_session()
        return l_conf

    def query_vice_conf(self, lordConfObj: object):
        session = self._db_engine.creat_session()
        v_conf = session.query(ViceData).filter(
            and_(ViceData.l_id == lordConfObj.id, ViceData.is_delete == 0)).all()
        self._db_engine.close_session()
        return v_conf

    def query_receiver_conf(self, confObj: object):
        session = self._db_engine.creat_session()
        r_conf = session.query(Receiver).filter(
            and_(Receiver.cId == confObj.id, Receiver.is_delete == 0)).all()
        self._db_engine.close_session()
        return r_conf

    def query_replace_data_conf(self, lordConfObj: object):
        session = self._db_engine.creat_session()
        rd_conf = session.query(ReplaceData).filter(
            and_(ReplaceData.l_id == lordConfObj.id, ReplaceData.is_delete == 0)).all()
        self._db_engine.close_session()
        return rd_conf

    def query_mapping_conf(self, lordid, viceid=None):
        session = self._db_engine.creat_session()
        if viceid:
            m_conf = session.query(MappingConf).filter(
                and_(MappingConf.l_id == lordid, MappingConf.v_id == viceid,
                     MappingConf.is_delete == 0)).all()
        else:
            m_conf = session.query(MappingConf).filter(
                and_(MappingConf.l_id == lordid, MappingConf.v_id == None,
                     MappingConf.is_delete == 0)).all()
        self._db_engine.close_session()
        return m_conf

    def query_busuness_conf(self, confobj: object):
        """
        传config数据库对象
        :param confobj:
        :return:
        """
        session = self._db_engine.creat_session()
        rd_conf = session.query(Busuness).filter(
            and_(Busuness.cId == confobj.id, Busuness.is_delete == 0)).all()
        self._db_engine.close_session()
        return rd_conf

    def query_busuness_first(self, confobj: object, table_title: str):
        """
        传config数据库对象
        :param confobj:
        :return:
        """
        session = self._db_engine.creat_session()
        rd_conf = session.query(Busuness).filter(
            and_(Busuness.cId == confobj.id, Busuness.is_delete == 0,
                 Busuness.table_title == table_title)).first()
        self._db_engine.close_session()
        return rd_conf


if __name__ == '__main__':
    AssemblyConfig()
