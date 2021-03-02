-- 每日回访名单 - 今日设置天气的蜂友
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