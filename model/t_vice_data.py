#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time:2021/2/11 22:23
# @Author: wei.zhang
# @File : t_vice_data.py
# @Software: PyCharm
from . import *


class ViceData(Base):
    __tablename__ = 't_vice_data'

    id = Column(Integer, autoincrement=True, nullable=False, primary_key=True, index=True)
    l_id = Column(Integer, ForeignKey("t_sub_busuness.id", ondelete="CASCADE"), nullable=False,
                  comment="主表配置id")
    data_sql = Column(Text, nullable=False, comment="执行SQL语句")
    data_name = Column(String(20), nullable=False, comment="sql描述")
    data_db_name = Column(String(20), nullable=False, comment="数据库名称")
    data_merge = Column(Boolean, default=False, comment="是否合并 False不合并，true合并")
    data_merge_key = Column(String(50), comment="合并字段，预留")
    createTime = Column(DateTime, nullable=False, server_default=func.now(), comment='记录创建时间')
    updateTime = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(),
                        comment='记录更新时间')
    is_delete = Column(SmallInteger, nullable=False, default=0, comment="是否删除，1删除 0未删除")
