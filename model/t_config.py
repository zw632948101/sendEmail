#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time:2021/2/11 22:20
# @Author: wei.zhang
# @File : t_config.py
# @Software: PyCharm
from model import *


class TConfig(Base):
    __tablename__ = 't_config'

    id = Column(Integer, autoincrement=True, nullable=False, primary_key=True, index=True)
    email_title = Column(String(50), nullable=False, comment="邮件标题")
    smtp_host = Column(String(50), nullable=False, comment="发送邮件host")
    conifg_name = Column(String(50), nullable=False, comment="配置名称")
    createTime = Column(DateTime, nullable=False, server_default=func.now(), comment='记录创建时间')
    updateTime = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(),
                        comment='记录更新时间')
    conf_version = Column(String(50), nullable=False, comment="配置版本")
    is_delete = Column(SmallInteger, nullable=False, default=0, comment="是否删除，1删除 0未删除")
    busuness = relationship('Busuness', backref='busuness_of_config')
    receiver = relationship('Receiver', backref="receiver_of_config")
