#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
__author__: wei.zhang
 @FILE     : sql.py
 @Time     : 2020/6/4 15:19
 @Software : PyCharm
"""

from DataBaseOperatePool import DataBaseOperate as db
from Log import Log


class sendEmailSQL(object):
    def __init__(self):
        super(sendEmailSQL, self).__init__()
        self.L = Log("ConfigInformationSql")
        self.db = db()
        self.db.creat_db_pool()

    def __del__(self):
        self.db.close_db_pool()

    def offline_promotion_personnel_statistics(self):
        sql = """
            SELECT tbf.user_name                                                                             as '姓名',
                   tbf.contact_number                                                                          as '手机号',
                   tc.value                                                                                    as '用户角色',
                   CONCAT((select tr.full_name from `fc-bee`.t_region tr where tbf.province = tr.id and tr.level = 0),
                   (select tr.full_name from `fc-bee`.t_region tr where tbf.city = tr.id and tr.level = 1),
                   (select tr.full_name from `fc-bee`.t_region tr where tbf.county = tr.id and tr.level = 2)) AS '省市区|县',
                   count(IF(to_days(tsi.create_time) = to_days(now()), 1, NULL))                               as '当日采集蜂场数量',
                   count(tsi.id)                                                                               as '累计采集蜂场数量'
            FROM `fc-bee`.t_user_role tur
                     INNER JOIN `fc-bee`.t_bee_friend tbf ON tur.user_id = tbf.user_id AND tbf.is_delete = 0
                     INNER JOIN `world-user`.t_user tu ON tur.user_id = tu.id AND tu.is_delete = 0
                     INNER JOIN `fc-bee`.t_config tc ON tur.role_code = tc.`key`
                     LEFT OUTER JOIN `fc-bee`.t_swarm_info tsi ON tur.user_id = tsi.creator_id AND tsi.is_delete = 0
            WHERE tur.is_delete = 0
              and tc.code = '10001'
              and tc.`key` in (1004,1005,1006)
            #   AND tu.status != 3
              AND tsi.from_type = 2
            group by tur.user_id
            order by 当日采集蜂场数量 DESC, tur.user_id ASC;
              """
        return self.db.query_data(sql)
