#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time:2021/3/1 17:02
# @Author: wei.zhang
# @File : t_busuness.py
# @Software: PyCharm

from model import *


class Busuness(Base):
    __tablename__ = 't_busuness'

    id = Column(Integer, autoincrement=True, nullable=False, primary_key=True, index=True)
    cId = Column(Integer, ForeignKey("t_config.id", ondelete="CASCADE"), nullable=False,
                 comment="主配置id")
    table_title = Column(String(50), nullable=False, comment="业务标题")
    createTime = Column(DateTime, nullable=False, server_default=func.now(), comment='记录创建时间')
    updateTime = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(),
                        comment='记录更新时间')
    is_delete = Column(SmallInteger, nullable=False, default=0, comment="是否删除，1删除 0未删除")
    sub_busuness = relationship('SubBusuness', backref='sub_busuness_of_config')
