/*
{"email_title":"追花族采集统计","statement_title":"每日采集统计","combine_label":"daily_statistics","combine":True,"combine_key":"联系方式"}
*/
        SELECT
       date_format(now(), '%Y-%m-%d')                               AS '采集日期',
       ctbf.real_name                                               AS '采集人',
       ctbf.contact_number                                          AS '联系方式',
       count(DISTINCT (tsi.id))                                     AS '采集蜂场数量',
       count(DISTINCT (stu.id))                                     AS '采集蜂友数量',
       count(DISTINCT if(stu.last_login_time IS NOT NULL, stu.id, NULL)) AS '登录蜂友数量',
       min(tsi.create_time)                                         AS '开始采集时间',
       max(tsi.create_time)                                         AS '结束采集时间',
       count(DISTINCT (tuns.creator_id))                            AS '推广蜂友天气设定人数',
       count(DISTINCT (thi.creator_id))                             AS '推广蜂友发布蜂友互助的数量_人',
       count(DISTINCT (thi.id))                                     AS '推广蜂友发布蜂友互助的数量_条数'
FROM `fc-bee`.t_swarm_info tsi
         LEFT JOIN `fc-bee`.t_bee_friend ctbf ON tsi.creator_id = ctbf.user_id AND ctbf.is_delete = 0
         LEFT JOIN `fc-bee`.t_user_role tur ON tsi.creator_id = tur.user_id AND tur.is_delete = 0
         LEFT JOIN `world-user`.t_user stu ON tsi.user_id = stu.id AND stu.is_delete = 0 AND stu.status <> 3 AND to_days(stu.create_time) = to_days(now()) AND stu.account_type = 21
         LEFT JOIN `fc-bee`.t_user_nectar_source tuns ON tuns.creator_id = stu.id AND tuns.is_delete = 0 AND to_days(tuns.create_time) = to_days(now())
         LEFT JOIN `fc-bee`.t_help_info thi ON thi.creator_id = tsi.user_id AND to_days(thi.create_time) = to_days(now())
WHERE tsi.is_delete = 0
  AND tur.role_code = 1006
  AND to_days(tsi.create_time) = to_days(now())
GROUP BY ctbf.user_id;
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

/*
{"email_title":"追花族采集统计","statement_title":"累计采集统计","combine_label":"add_up_statistics","combine":True,"combine_key":None}
*/
SELECT count(1) AS "当日新增蜂场数" FROM `fc-bee`.t_swarm_info WHERE is_delete=0 AND to_days(create_time) = to_days(now()) AND lat IS NOT NULL;
SELECT count(1) AS "当日新增蜂友数" FROM `world-user`.t_user WHERE is_delete=0 AND to_days(create_time) = to_days(now()) AND status<>3 AND account_type=21;
SELECT count(1) AS "当日登录蜂友数" FROM `world-user`.t_user WHERE is_delete=0 AND to_days(last_login_time) = to_days(now()) AND status<>3 AND account_type=21;
SELECT count(id) AS "当日调车次数",count(DISTINCT (user_id))AS "当日调车人数" FROM `fc-bee`.t_shunt WHERE is_delete=0 AND to_days(create_time) = to_days(now()) AND is_delete=0;
SELECT count(1) AS "当日蜂友互助信息条数",count(DISTINCT creator_id) AS "当日蜂友互助信息人数" FROM `fc-bee`.t_help_info WHERE to_days(create_time) = to_days(now());
SELECT count(DISTINCT creator_id) AS "当日设置天气的蜂友数" FROM `fc-bee`.t_user_nectar_source WHERE is_delete = 0 AND to_days(create_time) = to_days(now());
SELECT count(1) AS "累计蜂场数" FROM `fc-bee`.t_swarm_info WHERE is_delete=0 ;
SELECT count(1) AS "累计蜂友数" FROM `world-user`.t_user WHERE is_delete=0  AND status<>3 AND account_type=21;