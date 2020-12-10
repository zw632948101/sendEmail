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
{"email_title":"每日浅继箱回收统计","statement_title":"浅继箱回收汇总","combine_label":"assetRelease","combine":False,"combine_key":None,"DBname":"mp","DBstatus":False,"DBlist":[]}
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
{"email_title":"每日箱回收统计","statement_title":"浅继箱回收汇总","combine_label":"assetRelease","combine":False,"combine_key":None,"DBname":"mp","DBstatus":False,"DBlist":[]}
*/
SELECT a.create_time as '回收时间',u.`name` as '蜂友姓名',u.phone as '蜂友电话',count(l.id) as '回收数量/箱',
SUM(l.weight)/1000 as '回收重量/kg',(SUM(l.weight)-SUM(l.last_weight))/1000 as '回收蜜重/kg',u1.`name` as '操作人',a.address as '蜂场位置'
FROM `mp-asset`.t_asset_ledger_batch a,`mp-asset`.t_user_base u,`mp-asset`.t_asset_ledger l,`mp-asset`.t_user_base u1
WHERE a.type=30 AND a.cur_owner_type=2 AND a.last_owner_type=3 AND u.user_id=a.last_owner_id AND a.is_delete=0 AND l.is_delete=0
AND l.ledger_batch_id=a.id AND u1.user_id=a.creator_id
GROUP BY a.last_owner_id;