#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time:2021/2/11 22:24
# @Author: wei.zhang
# @File : t_receiver.py
# @Software: PyCharm
from . import *


class Receiver(Base):
    __tablename__ = 't_receiver'

    id = Column(Integer, autoincrement=True, nullable=False, primary_key=True, index=True)
    cId = Column(Integer, ForeignKey("t_config.id", ondelete="CASCADE"), nullable=False,
                   comment="主配置id")
    email = Column(String(50), nullable=False, comment="发送邮件")
    createTime = Column(DateTime, nullable=False, server_default=func.now(), comment='记录创建时间')
    updateTime = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(),
                        comment='记录更新时间')
    is_delete = Column(SmallInteger, nullable=False, default=0, comment="是否删除，1删除 0未删除")
