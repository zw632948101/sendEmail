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

    def __init__(self):
        super(Config, self).__init__()

    def get_config(self, name, current_path=None):
        if current_path is None:
            current_path = os.path.dirname(os.path.abspath(__file__))
        with open(current_path + "/" + name + ".yaml", encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return data

    def env_conf(self):
        return os.environ

    def get_yaml_dict(self, env_dict):
        env_dist = os.environ
        env_dict = env_dict.get(env_dist.get('EMAIL_ENV'))
        for key in env_dist:
            env_dict[key] = env_dist.get(key)
        return env_dict
