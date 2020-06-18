/*
{"email_title":"每日回访名单","statement_title":"今日登录的蜂友","combine_label":"daily_login_statistics","combine":False,"combine_key":None}
*/
SELECT if(tbf.real_name IS NOT NULL, tbf.real_name, tbf.user_name) AS '蜂友名称',
       tbf.contact_number                                          AS '联系方式',
       CASE tbf.from_type
           WHEN 1 THEN '主动注册'
           WHEN 2 THEN '员工添加'
           END                                                        '来源',
       tuls.count                                                  AS '当日登录次数',
       sum(tuls.count)                                             AS '累计登录次数',
       tbf.address                                                 AS '蜂友位置',
       count(ts.id)                                                AS '调车次数'
FROM `fc-bee`.t_user_login_statistics tuls
         LEFT JOIN `fc-bee`.t_bee_friend tbf ON tuls.user_id = tbf.user_id
         LEFT JOIN `fc-bee`.t_shunt ts ON ts.user_id = tbf.user_id AND ts.is_delete = 0
         LEFT JOIN `fc-bee`.t_user_role tsr ON tsr.user_id = tuls.user_id AND tsr.is_delete = 0
WHERE tbf.is_delete = 0
  AND to_days(tuls.edit_time) = to_days(now())
  AND tsr.role_code IS NULL
GROUP BY tbf.user_id;
/*
{"email_title":"每日回访名单","statement_title":"今日设置天气的蜂友","combine_label":"daily_weather_statistics","combine":False,"combine_key":None}
*/
SELECT if(tbf.real_name IS NOT NULL, tbf.real_name, tbf.user_name)                        AS '蜂友名称',
       tbf.contact_number                                                                 AS '联系方式',
       group_concat(if(tr_county.id IS NOT NULL, tr_county.full_name, tr_city.full_name)) AS '天气城市',
       tbf.address                                                                        AS '最后的登录位置'
FROM `fc-bee`.t_user_nectar_source tuns
         LEFT JOIN `fc-bee`.t_bee_friend tbf ON tbf.user_id = tuns.creator_id AND tbf.is_delete = 0 AND tbf.status <> 3
         LEFT JOIN `fc-bee`.t_region tr_city ON tr_city.id = tuns.city AND tr_city.is_delete = 0
         LEFT JOIN `fc-bee`.t_region tr_county ON tr_county.id = tuns.city AND tr_county.is_delete = 0
WHERE tuns.is_delete = 0
  AND tbf.user_id IS NOT NULL
  AND to_days(tuns.create_time) = to_days(now())
GROUP BY tuns.creator_id;
/*
{"email_title":"每日回访名单","statement_title":"今日调车的蜂友","combine_label":"daily_shunt_statistics","combine":False,"combine_key":None}
*/
SELECT if(tbf.real_name IS NOT NULL, tbf.real_name, tbf.user_name) AS '蜂友名称',
       tbf.contact_number                                          AS '联系方式',
       CASE ts.shunt_status
           WHEN 1 THEN '调车中'
           WHEN 2 THEN '已调车'
           WHEN 3 THEN '已取消'
           WHEN 4 THEN '已完成'
           END                                                        '调车状态',
       tsa_load.address                                            AS '出发地',
       tsa_unload.address                                          AS '目的地',
       ts.cancel_reasons                                           AS '取消原因',
       st.shunting_times                                           AS '历史调车次数',
       tbf.address                                                 AS '最后定位位置'
FROM `fc-bee`.t_shunt ts
         LEFT JOIN `fc-bee`.t_bee_friend tbf ON tbf.user_id = ts.user_id AND tbf.is_delete = 0 AND tbf.status <> 3
         LEFT JOIN (SELECT user_id, count(id) AS shunting_times FROM `fc-bee`.t_shunt WHERE is_delete = 0 GROUP BY user_id) st ON st.user_id = ts.user_id
         LEFT JOIN `fc-bee`.t_shunt_address tsa_load ON tsa_load.id = ts.load_address_id
         LEFT JOIN `fc-bee`.t_shunt_address tsa_unload ON tsa_unload.id = ts.unload_address_id
WHERE ts.is_delete = 0
  AND tbf.user_id IS NOT NULL
  AND to_days(now()) = to_days(ts.create_time);