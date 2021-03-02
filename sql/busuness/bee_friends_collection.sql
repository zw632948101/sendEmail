SELECT count(1) AS "累计蜂友数"
FROM `world-user`.t_user
WHERE is_delete = 0
  AND status <> 3
  AND account_type = 21;
SELECT count(1) AS "当日新增蜂友数"
FROM `world-user`.t_user
WHERE is_delete = 0
  AND to_days(create_time) = to_days(now())
  AND status <> 3
  AND account_type = 21;
SELECT count(1) AS "当日登录蜂友数"
FROM `world-user`.t_user
WHERE is_delete = 0
  AND to_days(last_login_time) = to_days(now())
  AND status <> 3
  AND account_type = 21;