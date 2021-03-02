SELECT b.create_time AS '合作时间', sum(b.number) AS '发放数量/箱', ba.`name` AS '蜂友姓名', ba1.name AS '操作人'
FROM `mp-asset`.t_asset_ledger_batch b,
     `mp-asset`.t_user_base ba,
     `mp-asset`.t_user_base ba1
WHERE b.cur_owner_id = ba.user_id
  AND b.cur_owner_type = 3
  AND b.type = 30
  AND b.creator_id = ba1.user_id
  AND b.is_delete = 0
GROUP BY b.create_time;