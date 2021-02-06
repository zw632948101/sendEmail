#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
__author__ = 'Heng Xin'
__date__ = '2018/3/28'
"""

from random import sample, choices


class DataConversion(object):

    @staticmethod
    def data_assemble(key=None, parameters_ld=None, num=None):
        """
        用于组装sql查询数据，取出相同的值返回该值的列表
        :param key:
        :param parameters_ld: 数据源为list字典
        :param num: 取出数据条数
        :return:
        """
        return_data = []
        if parameters_ld is None or num == 0:
            return
        # 判断num是否大于列表长度，小于时取列表长度
        num = len(parameters_ld) if num is None or num >= len(parameters_ld) else num

        if key:
            for info in sample(parameters_ld, num):
                if info.get(key):
                    return_data.append(info.get(key))
            if return_data:
                return sorted(return_data)
            else:
                return []
        return sample(parameters_ld, num)

    @staticmethod
    def del_dict_key(key, dt):
        """
        删除字典中指定的key
        :param key:要删除的key，可以为str和list
        :param dt:需要操作的数据，可以为dict和list
        :return:
        """
        if isinstance(key, str):
            key = [key]
        if isinstance(dt, dict):
            dt = [dt]
        del_key = lambda k, d: d.pop(k)

        def del_l_key(k: str, dt: list):
            _dl = []
            for d in dt:
                _dl.append(del_key(k, d))
            return _dl

        for k in key:
            del_l_key(k, dt)
        return dt

    @staticmethod
    def del_dict_value_null(dt):
        """
        删除字典中Value为空的键值对
        :param dt:
        :return:
        """

        def func(t):
            for i in list(t.keys()):
                if not t.get(i) and t.get(i) not in ('', 0):
                    del t[i]
            return t

        if isinstance(dt, dict):
            return func(dt)
        if isinstance(dt, list):
            dictlist = []
            for i in dt:
                dictlist.append(func(i))
            return dictlist

    @staticmethod
    def dict_chunk(dicts, size):
        new_list = []
        dict_len = len(dicts)
        while_count = dict_len // size + 1 if dict_len % size != 0 else dict_len / size
        split_start = 0
        split_end = size
        while (while_count > 0):
            new_list.append({k: dicts[k] for k in list(dicts.keys())[split_start:split_end]})
            split_start += size
            split_end += size
            while_count -= 1
        return new_list

    @staticmethod
    def replace_dict_value(replace_key, keep_dict, enumerate_dict: dict):
        """
        根据传入参数替换字段中值
        :param replace_key: 替换key
        :param keep_dict: 需要替换的数据，list or dict,其他类型数据直接返回源数据
        :param dict enumerate_dict: 替换枚举数据，dict
        :return: keep_dict
        """
        if isinstance(keep_dict, list):
            _dl = []
            for d in keep_dict:
                d[replace_key] = enumerate_dict.get(d.get(replace_key))
                _dl.append(d)
            keep_dict = _dl
        if isinstance(keep_dict, dict):
            keep_dict[replace_key] = enumerate_dict.get(keep_dict.get(replace_key))
        return keep_dict
