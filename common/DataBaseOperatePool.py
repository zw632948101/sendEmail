#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
@Time: 2020/04/02 19:43
@Author: guoyong
"""

import pymysql
import datetime
import decimal
from common.Log import Log
try:
    from DBUtils.PooledDB import PooledDB
except ModuleNotFoundError:
    from dbutils.pooled_db import PooledDB

class DataBaseOperate(object):

    def __init__(self):
        self.__log = Log("DataBaseOperate", 'DEBUG').logger
        self.__db_pool = None

    def creat_db_pool(self, mysql):
        user = mysql.get('MYSQL_USER')
        password = mysql.get('MYSQL_PASSWD')
        port = int(mysql.get('MYSQL_PORT'))
        host = mysql.get('MYSQL_HOST')
        self.__log.debug('创建数据库连接池：%s' % host)
        self.__db_pool = PooledDB(creator=pymysql,
                                  mincached=3,
                                  maxcached=5,
                                  maxshared=0,
                                  maxconnections=20,
                                  blocking=True,
                                  maxusage=None,
                                  setsession=None,
                                  host=host,
                                  port=port,
                                  user=user,
                                  db=None,
                                  passwd=password)
        self.__log.debug('创建数据库连接池完成!')

    def query_data(self, sql):
        con = self.__db_pool.connection()
        cursor = con.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            self.__log.error(sql)
            cursor.execute(sql)
            results = cursor.fetchall()
            self.__log.debug(results)
            for result in results:
                for fields in result:
                    if isinstance(result[fields], datetime.datetime):
                        result[fields] = str(result[fields].strftime('%Y-%m-%d %H:%M:%S'))
                    elif isinstance(result[fields], datetime.date):
                        result[fields] = str(result[fields].strftime('%Y-%m-%d'))
                    elif isinstance(result[fields], decimal.Decimal):
                        result[fields] = float(result[fields])
            return results
        except Exception as e:
            self.__log.error('执行sql异常：\n%s' % e)
            self.__log.error(sql)
        finally:
            cursor.close()
            con.close()

    def close_db_pool(self):
        self.__db_pool.close()
