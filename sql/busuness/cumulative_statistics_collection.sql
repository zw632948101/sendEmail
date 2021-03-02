SELECT count(1) AS "当日新增蜂场数"
FROM `fc-bee`.t_swarm_info
WHERE is_delete = 0
  AND to_days(create_time) = to_days(now())
  AND lat IS NOT NULL;
SELECT count(id) AS "当日调车次数", count(DISTINCT (user_id)) AS "当日调车人数"
FROM `fc-bee`.t_shunt
WHERE is_delete = 0
  AND to_days(create_time) = to_days(now())
  AND is_delete = 0;
SELECT count(1) AS "当日蜂友互助信息条数", count(DISTINCT creator_id) AS "当日蜂友互助信息人数"
FROM `fc-bee`.t_help_info
WHERE to_days(create_time) = to_days(now());
SELECT count(DISTINCT creator_id) AS "当日设置天气的蜂友数"
FROM `fc-bee`.t_user_nectar_source
WHERE is_delete = 0
  AND to_days(create_time) = to_days(now());
SELECT count(1) AS "累计蜂场数"
FROM `fc-bee`.t_swarm_info
WHERE is_delete = 0;