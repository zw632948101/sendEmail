#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time:2021/2/6 17:49
# @Author: wei.zhang
# @File : fileDir.py
# @Software: PyCharm
import os

# 主表存放路径
LORD_SQL = os.path.abspath(os.path.join(os.path.dirname(__file__), "../sql/busuness"))
# 副表存放路径
VICE_SQL = os.path.abspath(os.path.join(os.path.dirname(__file__), "../sql/viceData/"))
# SQL配置文件存放路径
SQL_CONFIG = os.path.abspath(os.path.join(os.path.dirname(__file__), "../sql/config/"))
# 配置数据库存放路径
CONFIG_DB = os.path.abspath(os.path.join(os.path.dirname(__file__), '../sql/dbDir/'))
# 运行配置文件路径
CONFIG = os.path.abspath(os.path.join(os.path.dirname(__file__), "../config/"))
# 枚举配置文件存放路径
ENUMERATE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../sql/enumerate/"))
# 生成附件存放路径
ATTACHMENT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../attachment/"))
