SELECT *
FROM (SELECT ctbf.real_name                                                                                  AS '采集人',
       date_format(min(if(to_days(tsi.create_time) = to_days(NOW()), tsi.create_time, NULL)), '%H:%i') AS '开始采集时间',
       date_format(max(if(to_days(tsi.create_time) = to_days(NOW()), tsi.create_time, NULL)), '%H:%i') AS '结束采集时间',
       count(if(to_days(tsi.create_time) = to_days(now()) AND tsi.creator_id = ctbf.user_id, 1, NULL)) AS '今日采集蜂场数',
       count(if(tsi.create_time >= '2021-01-20 00:00:00' AND tsi.creator_id = ctbf.user_id, 1, NULL))  AS '1月20日后采集蜂场数',
       count(if(tsi.user_id IN login_userid AND to_days(tsi.create_time) = to_days(NOW()), 1, NULL))             AS '今日采集蜂场登录数',
       count(if(tsi.user_id IN login_userid AND tsi.create_time >= '2021-01-20 00:00:00', 1, NULL))              AS '1月20日后采集蜂场今日登录数'
FROM `fc-bee`.t_swarm_info tsi
         LEFT JOIN (SELECT tbf.user_id, if(tbf.real_name IS NULL, tbf.user_name, tbf.real_name) AS real_name, tbf.contact_number
                    FROM `fc-bee`.t_bee_friend tbf
                             LEFT JOIN `fc-bee`.t_user_role tur ON tbf.user_id = tur.user_id AND tur.is_delete = 0
                    WHERE tbf.is_delete = 0 AND tur.user_id IS NOT NULL AND tur.role_code NOT IN (1008,1009)
                    GROUP BY tbf.user_id) ctbf ON tsi.creator_id = ctbf.user_id
WHERE tsi.is_delete = 0 AND ctbf.user_id IS NOT NULL
GROUP BY tsi.creator_id
ORDER BY count(if(to_days(tsi.create_time) = to_days(now()), 1, NULL)) DESC) t
WHERE t.今日采集蜂场数 > 0;