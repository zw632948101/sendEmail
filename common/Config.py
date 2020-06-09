#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
__author__: wei.zhang
 @FILE     : Config.py
 @Time     : 2020/6/4 14:46
 @Software : PyCharm
"""
import os

import yaml


class Config(object):

    def __init__(self, name, current_path=None):
        self.name = name
        if current_path is None:
            current_path = os.path.dirname(os.path.abspath(__file__))
        with open(current_path + "/" + name + ".yaml", encoding='utf-8') as f:
            self.data = yaml.safe_load(f)

    @staticmethod
    def get_yaml_dict():
        env = Config('config').data.get('env')
        env_dist = os.environ
        env_dict = Config('config').data.get(env)
        env_dict['MYSQL_PASSWD'] = env_dist.get('MYSQL_PASSWD')
        env_dict['EMAIL_PASSWD'] = env_dist.get('EMAIL_PASSWD')
        return env_dict
