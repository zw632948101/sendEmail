-- 每日采集蜂友统计 - 每日登陆数据
SELECT tlt.user_id
FROM `world-passport`.t_login_token tlt
         LEFT JOIN `world-user`.t_user tu ON tlt.user_id = tu.id AND tu.account_type = 21
WHERE to_days(tlt.create_time) = to_days(now())
GROUP BY tlt.user_id;