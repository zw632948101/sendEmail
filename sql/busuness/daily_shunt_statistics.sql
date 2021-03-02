-- 每日回访名单 - 今日调车的蜂友
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
         LEFT JOIN `fc-bee`.t_bee_friend tbf
                   ON tbf.user_id = ts.user_id AND tbf.is_delete = 0 AND tbf.status <> 3
         LEFT JOIN (SELECT user_id, count(id) AS shunting_times
                    FROM `fc-bee`.t_shunt
                    WHERE is_delete = 0
                    GROUP BY user_id) st ON st.user_id = ts.user_id
         LEFT JOIN `fc-bee`.t_shunt_address tsa_load ON tsa_load.id = ts.load_address_id
         LEFT JOIN `fc-bee`.t_shunt_address tsa_unload ON tsa_unload.id = ts.unload_address_id
WHERE ts.is_delete = 0
  AND tbf.user_id IS NOT NULL
  AND to_days(now()) = to_days(ts.create_time);