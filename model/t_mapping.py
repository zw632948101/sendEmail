#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time:2021/2/26 14:21
# @Author: wei.zhang
# @File : t_mapping.py
# @Software: PyCharm
from . import *


class MappingConf(Base):
    __tablename__ = 't_mapping_conf'

    id = Column(Integer, autoincrement=True, nullable=False, primary_key=True, index=True)
    l_id = Column(Integer, ForeignKey("t_sub_busuness.id", ondelete="CASCADE"), nullable=False,
                  comment="主表配置id")
    v_id = Column(Integer, ForeignKey("t_vice_data.id", ondelete="CASCADE"), comment="副表配置id")
    mapping_key = Column(String(50), comment='需要映射的字段')
    mapping_file = Column(String(50), comment="需要映射的文件")
    createTime = Column(DateTime, nullable=False, server_default=func.now(), comment='记录创建时间')
    updateTime = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(),
                        comment='记录更新时间')
    is_delete = Column(SmallInteger, nullable=False, default=0, comment="是否删除，1删除 0未删除")
