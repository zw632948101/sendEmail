#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time:2021/2/11 22:20
# @Author: wei.zhang
# @File : t_sub_busuness.py
# @Software: PyCharm
from model import *


class SubBusuness(Base):
    __tablename__ = 't_sub_busuness'

    id = Column(Integer, autoincrement=True, nullable=False, primary_key=True, index=True)
    b_id = Column(Integer, ForeignKey("t_busuness.id", ondelete="CASCADE"), nullable=False,
                  comment="业务id")
    merge_key = Column(String(50), comment="合并key")
    busuness_sql = Column(Text, nullable=False, comment="执行SQL语句")
    busuness_name = Column(String(20), nullable=False, comment="sql描述")
    merge = Column(Boolean, nullable=False, default=False, comment="是否合并 False不合并，true合并")
    bus_vice_merge = Column(Boolean, nullable=False, default=False, comment="是否合并 False不合并，true合并")
    bus_vice_merge_key = Column(String(20), comment="数据表合并")
    db_name = Column(String(20), nullable=False, comment="数据库名称")
    createTime = Column(DateTime, nullable=False, server_default=func.now(), comment='记录创建时间')
    updateTime = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(),
                        comment='记录更新时间')
    is_delete = Column(SmallInteger, nullable=False, default=0, comment="是否删除，1删除 0未删除")
    vice = relationship('ViceData', backref='vice_data_of_lord')
    replace_data = relationship('ReplaceData', backref='t_replace_data_of_lord')
