-- 资产发放统计 - 历史蜂友蜂场数据查询
SELECT date_format(b.create_time, '%Y-%m-%d') AS '合作时间',
       sum(b.number)                          AS '发放数量/箱',
       ba.`name`                              AS '蜂友姓名',
       ba.phone                               AS '蜂友电话',
       b.creator_id                           AS '操作人',
       b.apiary_id                            AS '蜂场id'
FROM `mp-asset`.t_asset_ledger_batch b,
     `mp-asset`.t_user_base ba
WHERE b.cur_owner_id = ba.user_id
  AND b.cur_owner_type = 3
  AND b.type = 30
  AND b.is_delete = 0
  AND ba.is_delete = 0
GROUP BY date_format(b.create_time, '%Y-%m-%d'), b.cur_owner_id;