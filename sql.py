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
from DataAggregate import DataAggregate


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

    @property
    def flowers_collection_statistics(self) -> list:
        """
        追花采集统计
        :return: 项目专员每人的采集结果
        """
        aggregate_data = DataAggregate()
        # 当日采集
        that_day_sql = """
        SELECT date_format(now(), '%Y-%m-%d')                                               AS '采集日期',
       ctbf.real_name                                                               AS '采集人',
       ctbf.contact_number                                                          AS '联系方式',
       count(DISTINCT (tsi.id))                                                     AS '采集蜂场数量',
       count(DISTINCT (tsi.user_id))                                                AS '采集蜂友数量',
       count(DISTINCT (if(to_days(stu.last_login_time) = to_days(now()), 1, NULL))) AS '登录蜂友数量',
       min(tsi.create_time)                                                         AS '开始采集时间',
       max(tsi.create_time)                                                         AS '结束采集时间',
       count(DISTINCT (tuns.creator_id))                                                    AS '推广蜂友天气设定人数',
       count(DISTINCT (thi.creator_id))                                             AS '推广蜂友发布蜂友互助的数量_人',
       count(DISTINCT (thi.id))                                                     AS '推广蜂友发布蜂友互助的数量_条数'
FROM `fc-bee`.t_swarm_info tsi
         LEFT JOIN `fc-bee`.t_bee_friend ctbf ON tsi.creator_id = ctbf.user_id AND ctbf.is_delete = 0
         LEFT JOIN `fc-bee`.t_user_role tur ON tsi.creator_id = tur.user_id AND tur.is_delete = 0
         LEFT JOIN `world-user`.t_user stu ON tsi.user_id = stu.id AND stu.is_delete = 0 AND stu.status <> 3 AND stu.account_type = 21
         LEFT JOIN `fc-bee`.t_user_nectar_source tuns ON tuns.creator_id = tsi.user_id AND tuns.is_delete = 0
         LEFT JOIN `fc-bee`.t_help_info thi ON thi.creator_id = tsi.user_id
WHERE tsi.is_delete = 0
  AND tur.role_code = 1006
  AND to_days(tsi.create_time) = to_days(now())
GROUP BY ctbf.user_id;
        """
        add_up_sql = """
        SELECT
       ctbf.contact_number                                                          AS '联系方式',
       ctbf.real_name                                                               AS '采集人',
       count(DISTINCT (tsi.id))                                                     AS '6月1号后累计蜂场数量',
       count(DISTINCT (tsi.user_id))                                                AS '6月1号后累计采集蜂友数量'
FROM `fc-bee`.t_swarm_info tsi
         LEFT JOIN `fc-bee`.t_bee_friend ctbf ON tsi.creator_id = ctbf.user_id AND ctbf.is_delete = 0
         LEFT JOIN `fc-bee`.t_user_role tur ON tsi.creator_id = tur.user_id AND tur.is_delete = 0
WHERE tsi.is_delete = 0
  AND tur.role_code = 1006
  AND tsi.create_time >= '2020-06-01 00:00:00'
GROUP BY ctbf.user_id;
        """

        that_day_result = self.db.query_data(that_day_sql)
        add_up_result = self.db.query_data(add_up_sql)

        return aggregate_data.get_aggregate_result(add_up_result,
                                                   that_day_result,
                                                   key='联系方式')
