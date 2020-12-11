/*
{"email_title":"每日浅继箱回收统计","statement_title":"浅继箱回收明细","combine_label":"assetRelease","combine":False,"combine_key":None,"DBname":"mp","DBstatus":False,"DBlist":[]}
*/
SELECT a.create_time                               AS '回收时间',
       u.`name`                                    AS '蜂友姓名',
       u.phone                                     AS '蜂友电话',
       count(l.id)                                 AS '回收数量/箱',
       SUM(l.weight) / 1000                        AS '回收重量/kg',
       (SUM(l.weight) - SUM(l.last_weight)) / 1000 AS '回收蜜重/kg',
       u1.`name`                                   AS '操作人',
       a.address                                   AS '蜂场位置'
FROM `mp-asset`.t_asset_ledger_batch a,
     `mp-asset`.t_user_base u,
     `mp-asset`.t_asset_ledger l,
     `mp-asset`.t_user_base u1
WHERE a.type = 30
  AND a.cur_owner_type = 2
  AND a.last_owner_type = 3
  AND u.user_id = a.last_owner_id
  AND a.is_delete = 0
  AND l.is_delete = 0
  AND l.ledger_batch_id = a.id
  AND u1.user_id = a.creator_id
  AND TO_DAYS(a.create_time) = TO_DAYS(NOW())
GROUP BY a.last_owner_id;

/*
{"email_title":"每日箱回收统计","statement_title":"浅继箱回收历史","combine_label":"assetRelease","combine":False,"combine_key":None,"DBname":"mp","DBstatus":False,"DBlist":[]}
*/
SELECT a.create_time as '回收时间',u.`name` as '蜂友姓名',u.phone as '蜂友电话',count(l.id) as '回收数量/箱',
SUM(l.weight)/1000 as '回收重量/kg',(SUM(l.weight)-SUM(l.last_weight))/1000 as '回收蜜重/kg',u1.`name` as '操作人',a.address as '蜂场位置'
FROM `mp-asset`.t_asset_ledger_batch a,`mp-asset`.t_user_base u,`mp-asset`.t_asset_ledger l,`mp-asset`.t_user_base u1
WHERE a.type=30 AND a.cur_owner_type=2 AND a.last_owner_type=3 AND u.user_id=a.last_owner_id AND a.is_delete=0 AND l.is_delete=0
AND l.ledger_batch_id=a.id AND u1.user_id=a.creator_id
GROUP BY a.create_time
ORDER BY a.create_time DESC;

/*
{"email_title":"每日浅继箱回收统计","statement_title":"浅继箱业务数据汇总","combine_label":"assetRelease","combine":False,"combine_key":None,"DBname":"mp","DBstatus":False,"DBlist":[]}
*/
SELECT af.name AS '蜂友姓名', af.phone AS '蜂友电话', af.NUMBER AS '发放箱数', ah.number AS '累积回收蜜脾数'
FROM (SELECT uu.name, uu.phone, SUM(aa.number) AS NUMBER, aa.cur_owner_id
      FROM `mp-asset`.t_asset_ledger_batch aa,
           `mp-asset`.t_user_base uu
      WHERE aa.type = 30
        AND aa.cur_owner_type = 3
        AND aa.last_owner_type = 2
        AND aa.cur_owner_id = uu.user_id
        AND aa.is_delete = 0
      GROUP BY aa.cur_owner_id) af
         LEFT OUTER JOIN
     (SELECT last_owner_id, SUM(number) AS number
      FROM `mp-asset`.t_asset_ledger_batch
      WHERE type = 30
        AND cur_owner_type = 2
        AND last_owner_type = 3
        AND is_delete = 0
      GROUP BY last_owner_id) ah
     ON ah.last_owner_id = af.cur_owner_id;

/*
{"email_title":"每日浅继箱回收统计","statement_title":"浅继箱业务合并统计","combine_label":"assetRelease","combine":False,"combine_key":None,"DBname":"mp","DBstatus":False,"DBlist":[]}
*/
SELECT
	aaa.`name` AS '蜂友姓名',
	aaa.address AS '蜂场位置',
	aaa.phone AS '蜂友电话',
	aaa.number_all_fa AS '发放箱数/箱',
	aaa.now_day AS '当日回收浅继箱数',
	aaa.now_weight_all AS '当日回收重量',
	aaa.now_weight_mi AS '当日回收蜜重',
	ccc.all_number AS '累积回收浅继箱数',
	ccc.all_weight AS '累积回收重量',
	ccc.weight_mi_all AS '累积回收蜜重',
	( ccc.weight_mi_all / ccc.all_number ) AS '平均每箱重量',
	( aaa.number_all_fa - IFNULL( ccc.all_number, 0 ) ) AS '待回收数量'
FROM
	(
SELECT
	aa.*,
	bb.*
FROM
	(
SELECT
	ba.`name`,
	b.address,
	ba.phone,
	sum( b.number ) AS number_all_fa,
	b.cur_owner_id
FROM
	`mp-asset`.t_asset_ledger_batch b,
	`mp-asset`.t_user_base ba
WHERE
	b.cur_owner_id = ba.user_id
	AND b.cur_owner_type = 3
	AND b.type = 30
	AND b.is_delete = 0
	AND b.last_owner_type = 2
GROUP BY
	b.cur_owner_id
	) aa
	LEFT OUTER JOIN (
SELECT
	count( l.id ) AS now_day,
	a.last_owner_id AS user_ID,
	SUM( l.weight ) / 1000 AS now_weight_all,
	( SUM( l.weight ) - SUM( l.last_weight ) ) / 1000 AS now_weight_mi
FROM
	`mp-asset`.t_asset_ledger_batch a,
	`mp-asset`.t_asset_ledger l
WHERE
	a.type = 30
	AND a.cur_owner_type = 2
	AND a.last_owner_type = 3
	AND a.is_delete = 0
	AND l.is_delete = 0
	AND l.ledger_batch_id = a.id
	AND TO_DAYS( a.create_time ) = TO_DAYS( NOW( ) )
GROUP BY
	a.last_owner_id
	) bb ON bb.user_ID = aa.cur_owner_id
	) aaa
	LEFT OUTER JOIN (
SELECT
	count( l.id ) AS all_number,
	a.last_owner_id,
	SUM( l.weight ) / 1000 AS all_weight,
	( SUM( l.weight ) - SUM( l.last_weight ) ) / 1000 AS weight_mi_all
FROM
	`mp-asset`.t_asset_ledger_batch a,
	`mp-asset`.t_asset_ledger l
WHERE
	a.type = 30
	AND a.cur_owner_type = 2
	AND a.last_owner_type = 3
	AND a.is_delete = 0
	AND l.is_delete = 0
	AND l.ledger_batch_id = a.id 
GROUP BY
	a.last_owner_id
	) ccc ON ccc.last_owner_id = aaa.cur_owner_id;