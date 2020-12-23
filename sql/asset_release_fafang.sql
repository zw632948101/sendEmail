/*
{"email_title":"资产回收统计","statement_title":"浅继箱业务汇总","combine_label":"test","combine":False,"combine_key":None,"LORD_VICE_MERGE":False,"VICE_MERGE":True,"DBname":"flower","DBstatus":True,"DBlist":[{"DBname":"mp","sqlfile":"hui_shou_hui_zong.sql","db_key":[{"Value":"product_no","replace":"relation_no_list1"},{"Value":"product_no1","replace":"relation_no_list2"}],"MERGE_KEY":'user_id'},{"DBname":"flower","sqlfile":"shallow_check.sql","db_key":[],"MERGE_KEY":'user_id'}]}
*/
SELECT product_no
FROM `fc-trade`.t_product
WHERE IFNULL(cap_rate, 0) >= 90
  AND is_delete = 0;
SELECT product_no AS product_no1
FROM `fc-trade`.t_product
WHERE IFNULL(cap_rate, 0) < 90
  AND is_delete = 0;
/*
{"email_title":"资产回收统计","statement_title":"当日浅继箱回收明细","combine_label":"test","combine":False,"combine_key":None,"LORD_VICE_MERGE":False,"VICE_MERGE":False,"DBname":"flower","DBstatus":True,"DBlist":[{"DBname":"mp","sqlfile":"dang_ri_hui_shou.sql","db_key":[{"Value":"product_no","replace":"relation_no_list1"},{"Value":"product_no1","replace":"relation_no_list2"}],"MERGE_KEY":None}]}
*/
SELECT product_no
FROM `fc-trade`.t_product
WHERE IFNULL(cap_rate, 0) >= 90
  AND is_delete = 0;
SELECT product_no AS product_no1
FROM `fc-trade`.t_product
WHERE IFNULL(cap_rate, 0) < 90
  AND is_delete = 0;
/*
{"email_title":"资产回收统计","statement_title":"历史浅继箱回收明细","combine_label":"test","combine":False,"combine_key":None,"LORD_VICE_MERGE":False,"VICE_MERGE":False,"DBname":"mp","DBstatus":False,"DBlist":[]}
*/
SELECT a.create_time        AS '回收时间',
       u.`name`             AS '蜂友姓名',
       count(l.id)          AS '回收数量/箱',
       SUM(l.weight) / 1000 AS '回收重量/kg',
       CASE
           WHEN IFNULL(SUM(l.weight) / 1000, 0) = 0 THEN
               0
           ELSE
                   (SUM(l.weight) - SUM(l.last_weight)) / 1000
           END                 '回收蜜重/kg',
       CASE
           WHEN IFNULL(SUM(l.weight) / 1000, 0) != 0 THEN
               FORMAT((SUM(l.weight) - SUM(l.last_weight)) / 1000 / count(l.id), 2)
           END                 '平均回收蜜重/kg',
       u1.`name`            AS '操作人',
       a.address            AS '蜂场位置'
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
GROUP BY a.create_time
ORDER BY a.create_time DESC;
/*
{"email_title":"资产回收统计","statement_title":"浅继箱发放明细","combine_label":"test","combine":False,"combine_key":None,"LORD_VICE_MERGE":False,"VICE_MERGE":False,"DBname":"mp","DBstatus":False,"DBlist":[]}
*/
SELECT b.create_time AS '合作时间', sum(b.number) AS '发放数量/箱', ba.`name` AS '蜂友姓名', ba1.name AS '操作人'
FROM `mp-asset`.t_asset_ledger_batch b,
     `mp-asset`.t_user_base ba,
     `mp-asset`.t_user_base ba1
WHERE b.cur_owner_id = ba.user_id
  AND b.cur_owner_type = 3
  AND b.type = 30
  AND b.creator_id = ba1.user_id
  AND b.is_delete=0
GROUP BY b.create_time;