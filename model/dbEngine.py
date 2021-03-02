#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fileDir.fileDir import CONFIG_DB
from model import Base
from pathlib import Path
import os


class DBEngine(object):
    def __init__(self):
        # 初始化数据库链接
        if not Path(CONFIG_DB).is_dir():
            os.mkdir(CONFIG_DB)
        self.dataBaseURI = f'sqlite:///{CONFIG_DB}/sendEmail.db'
        self.__engine = create_engine(self.dataBaseURI, echo=False)
        Base.metadata.create_all(self.__engine)
        self.session = None

    def creat_session(self):
        self.session = sessionmaker(bind=self.__engine)()
        return self.session

    def close_session(self):
        self.session.close()
        return "OK"
