#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time:2021/2/25 10:40
# @Author: wei.zhang
# @File : t_replace_data.py
# @Software: PyCharm
from . import *


class ReplaceData(Base):
    __tablename__ = 't_replace_data'
    id = Column(Integer, autoincrement=True, nullable=False, primary_key=True, index=True)
    l_id = Column(Integer, ForeignKey("t_sub_busuness.id", ondelete="CASCADE"), nullable=False,
                  comment="主表配置id")
    condition_value = Column(String(20), nullable=False, comment="条件数据key")
    replace_value = Column(String(20), nullable=False, comment="替换提交key")
    createTime = Column(DateTime, nullable=False, server_default=func.now(), comment='记录创建时间')
    updateTime = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(),
                        comment='记录更新时间')
    is_delete = Column(SmallInteger, nullable=False, default=0, comment="是否删除，1删除 0未删除")
