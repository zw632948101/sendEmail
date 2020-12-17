/*
{"email_title":"追花族上下班打卡","statement_title":"每日上下班打卡统计","combine_label":"ClockInAndOutStatistics","combine":False,"combine_key":None}
*/
SELECT user_all1.real_name as '姓名',user_all1.value as '角色',user_all1.contact_number as '手机号',user_all1.lng,user_all1.lat,
user_all1.shangbandaka as '上班打卡',before_ka1.xiabandaka as '下班打卡',user_all1.address as '打卡地址' FROM
(SELECT user_all.*,before_ka.* FROM
(SELECT f.real_name,f.contact_number,c.`value`,f.user_id
FROM `fc-bee`.t_bee_friend f,`fc-bee`.t_user_role r,`fc-bee`.t_config c
WHERE r.user_id=f.user_id AND c.`key`=r.role_code AND c.`code`=10001 AND r.role_code IN (1007,1005,1006)
AND f.is_delete=0 AND r.is_delete=0 AND c.is_delete=0) user_all LEFT OUTER JOIN
(SELECT user_id as userID,lng,lat,create_time as shangbandaka,address
FROM `fc-bee`.t_staff_trail
WHERE TO_DAYS(create_time) = TO_DAYS(NOW()) AND type=2 AND is_delete=0) before_ka
ON before_ka.userID=user_all.user_id) user_all1 LEFT OUTER JOIN
(SELECT user_id as user_ID,max(create_time) as xiabandaka
FROM `fc-bee`.t_staff_trail
WHERE TO_DAYS(create_time) = TO_DAYS(NOW())-1 AND type=3 AND is_delete=0
GROUP BY user_id) before_ka1
ON before_ka1.user_ID=user_all1.user_id;