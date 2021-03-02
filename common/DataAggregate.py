#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time:2020/11/23 09:55
# @Author: wei.zhang
# @File : DataAggregate.py
# @Software: PyCharm
from random import sample

from common.Log import Log


class DataAggregate(object):
    def __init__(self):
        self.__tmp_date = set()
        self.__operate_list_dict = list()
        self.__result = list()
        self.__key = ""
        # 按传入当参数类型进行聚合,入参形式[{},{},{}]
        # 只找第一个匹配当数据，之后数据丢弃处理
        # 返回数据格式是[{},{},{}]
        self.L = Log("DataAggregate")

    def __key_suit(self):
        for i in self.__operate_list_dict:
            if i is not None:
                for j in i:
                    self.__tmp_date.add(j.get(self.__key))
        try:
            self.__tmp_date.remove(None)
        except KeyError:
            pass
        finally:
            if len(self.__tmp_date) == 0:
                self.L.logger.warning("分类参数不在数据中")

    def __do_aggregate(self) -> None:
        self.__result = list()
        self.__key_suit()
        self.__tmp_date = list(self.__tmp_date)
        self.__tmp_date.sort()

        for i in range(len(self.__tmp_date)):
            self.__result.append({self.__key: self.__tmp_date[i]})

            for j in self.__operate_list_dict:
                if j is not None:
                    for k in j:
                        if self.__tmp_date[i] == k.get(self.__key):
                            self.__result[i].update(k)
                            del self.__operate_list_dict[self.__operate_list_dict.index(j)][
                                j.index(k)]
                            break

    def get_aggregate_result(self, *operate_list_dict: list, key: str) -> list:
        if len(operate_list_dict) > 1:
            self.__operate_list_dict = operate_list_dict
            self.__key = key
            self.__do_aggregate()
        else:
            try:
                self.__result = operate_list_dict[0]
            except IndexError:
                pass
            finally:
                self.__result = []

        self.__tmp_date = list()
        self.__operate_list_dict = list()
        self.__key = ""
        return self.__result

    def get_aggregate_result_copy(self, operate_list_dict: list, key: str) -> list:
        if len(operate_list_dict) > 1:
            self.__operate_list_dict = operate_list_dict
            self.__key = key
            self.__do_aggregate()
        else:
            try:
                self.__result = operate_list_dict[0]
            except IndexError:
                pass
            finally:
                self.__result = []

        self.__tmp_date = set()
        self.__operate_list_dict = list()
        self.__key = ""
        return self.__result

    def Master_schedule_aggregate(self, operate_list_dict, key):
        """
        主附表合并
        :param operate_list_dict: 第一个表为主表，第二个表为附表
        :param key: 合并字段
        :return:
        """
        result = []
        list1, list2 = operate_list_dict
        for l1 in list1:
            for l2 in list2:
                if isinstance(l2, list):
                    self.Master_schedule_aggregate([list1, l2])
                if l1.get(key) == l2.get(key):
                    l1.update(l2)
                result.append(l1)
        return result

    @staticmethod
    def valueNull(dt):
        """
        删除字典中Value为空的键值对
        :param dt:
        :return:
        """

        def func(t):
            for i in list(t.keys()):
                if not t.get(i) and t.get(i) not in ('', 0):
                    t[i] = '0'
            return t

        if isinstance(dt, dict):
            return func(dt)
        if isinstance(dt, list):
            dictlist = []
            for i in dt:
                dictlist.append(func(i))
            return dictlist

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
