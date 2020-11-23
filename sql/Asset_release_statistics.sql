/*
{"email_title":"资产发放统计","statement_title":"每日资产发放统计","combine_label":"AssetReleaseStatistics","combine":False,"combine_key":None,"DBname":"mp","DBstatus":True,"DBlist":[{"DBname":"flower","sqlfile":"creator_name.sql","db_key":"操作人","replace":"creator_id"}]}
*/
SELECT b.create_time AS '合作时间', sum(b.number) AS '发放数量/箱', ba.`name` AS '蜂友姓名', ba.phone AS '蜂友电话', b.creator_id AS '操作人'
FROM `mp-asset`.t_asset_ledger_batch b,
     `mp-asset`.t_user_base ba
WHERE TO_DAYS(b.create_time) = TO_DAYS(NOW())
  AND b.cur_owner_id = ba.user_id
  AND b.cur_owner_type = 3
  AND b.type = 30
GROUP BY b.cur_owner_id;