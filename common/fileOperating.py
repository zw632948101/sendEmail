#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time:2020/12/15 14:49
# @Author: wei.zhang
# @File : fileOperating.py
# @Software: PyCharm
import os
import shutil
from fileDir.fileDir import ATTACHMENT


class FileOperating(object):
    def __init__(self):
        super(FileOperating, self).__init__()

    def del_file(self, filepath=ATTACHMENT):
        """
        删除某一目录下的所有文件或文件夹
        :param filepath: 路径
        :return:
        """
        try:
            os.listdir(filepath)
        except FileNotFoundError:
            os.mkdir(filepath)
        del_list = os.listdir(filepath)
        for f in del_list:
            file_path = os.path.join(filepath, f)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    def read_file(self, filepath):
        with open(filepath, encoding='utf-8') as f:
            datas = f.read()
        return datas
