#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time:2021/2/11 22:20
# @Author: wei.zhang
# @File : __init__.py.py
# @Software: PyCharm

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Integer, func, SmallInteger, ForeignKey, Text, \
    table, Boolean
from sqlalchemy.orm import relationship

Base = declarative_base()
