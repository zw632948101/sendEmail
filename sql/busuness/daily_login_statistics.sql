-- 每日回访名单 - 今日登录的蜂友
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