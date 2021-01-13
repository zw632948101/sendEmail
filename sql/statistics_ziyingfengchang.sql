/*
{"email_title":"自营蜂场统计","statement_title":"自营蜂场统计","combine_label":"statisticsZiYingFengChang","combine":False,"combine_key":None}
*/
SELECT
	a.*,
	b.NAME AS '封箱负责人'
FROM
	(
SELECT
	h.serial_no,
	max( o.operate_time ) AS time,
	f.real_name AS '盘点助理',
	IFNULL( f1.real_name, f1.user_name ) AS '盘点养蜂老师',
	CONCAT( r.full_name, r1.full_name, r2.full_name ) AS '位置(省市区)',
	o.address AS '详细地址',
	h.baby_num AS '子脾数量',
CASE
	h.disease
	WHEN 1 THEN
	'蜂群健康'
	WHEN 2 THEN
	'大蜂螨'
	WHEN 3 THEN
	'小蜂螨'
	WHEN 4 THEN
	'白垩病' ELSE '其他'
	END '病害信息',
CASE
	h.queen_num
	WHEN 1 THEN
	'双王'
	WHEN 2 THEN
	'单王' ELSE '失王'
	END '蜂王数量',
CASE
	h.queen_lock
	WHEN 1 THEN
	'已关王'
	WHEN 0 THEN
	'未关王' ELSE NULL
	END '是否关王'
FROM
	`fc-bee`.t_hive_baby h,
	`fc-bee`.t_bee_friend f,
	`fc-bee`.t_bee_friend f1,
	`fc-bee`.t_hive_log_open o,
	`fc-bee`.t_region r,
	`fc-bee`.t_region r1,
	`fc-bee`.t_region r2
WHERE
	h.is_delete = 0
	AND h.last_open_time IS NOT NULL
	AND h.checker_id = f.user_id
	AND o.hive_no = h.serial_no
	AND o.is_delete = 0
	AND f1.user_id = o.keeper_id
	AND r.id = o.province
	AND r1.id = o.city
	AND r2.id = o.county
GROUP BY
	serial_no
ORDER BY
	o.operate_time DESC
	) a
	LEFT OUTER JOIN (
SELECT
	l.hive_no,
	IFNULL( f.real_name, f.user_name ) AS NAME,
	max( l.bind_time ) AS 'real_time'
FROM
	`fc-bee`.t_bee_friend f,
	`fc-bee`.t_hive_log_bind l
WHERE
	l.is_delete = 0
	AND f.is_delete = 0
	AND l.owner_id = f.user_id
GROUP BY
	l.hive_no
	) b ON b.hive_no = a.serial_no
ORDER BY
	a.time DESC;