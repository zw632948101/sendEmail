/*
{"email_title":"追花族上下班打卡","statement_title":"每日上下班打卡统计","combine_label":"ClockInAndOutStatistics","combine":False,"combine_key":None}
*/
SELECT a.real_name AS '姓名', a.contact_number AS '手机号', a.create_time AS '上班打卡', b.endtime AS '下班打卡', a.lng, a.lat
FROM (SELECT t.real_name,
             t.contact_number,
             CASE s.type
                 WHEN 2 THEN
                     '上班打卡'
                 WHEN 3 THEN
                     '下班打卡'
                 ELSE
                     '普通定位'
                 END 'typeStr',
             s.create_time,
             s.user_id,
             s.lng,
             s.lat
      FROM `fc-bee`.t_bee_friend t,
           `fc-bee`.t_staff_trail s
      WHERE t.user_id = s.user_id
        AND s.type = 2
        AND TO_DAYS(s.create_time) = TO_DAYS(NOW())) a
         LEFT OUTER JOIN
     (SELECT user_id, max(create_time) AS endtime
      FROM `fc-bee`.t_staff_trail
      WHERE type = 3
        AND TO_DAYS(create_time) = TO_DAYS(NOW())
      GROUP BY user_id) b
     ON a.user_id = b.user_id
         LEFT OUTER JOIN `fc-bee`.t_user_role tu ON a.user_id = tu.user_id AND tu.is_delete = 0 AND tu.role_code IN (1004, 1005, 1006, 1007)