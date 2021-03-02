-- 资产回收统计 - 历史浅继箱回收明细
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