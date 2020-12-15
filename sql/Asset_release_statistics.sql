/*
{"email_title":"资产发放统计","statement_title":"每日资产发放统计","combine_label":"AssetReleaseStatistics","combine":False,"combine_key":None,"LORD_VICE_MERGE":True,"VICE_MERGE":False,"DBname":"mp","DBstatus":True,"DBlist":[{"DBname":"flower","sqlfile":"creator_name.sql","db_key":[{"Value":"操作人","replace":"操作人list"}],"MERGE_KEY":"操作人"},{"DBname":"flower","sqlfile":"asset_release_apiary_info.sql","db_key":[{"Value":"蜂场id","replace":"swarmid"}],"MERGE_KEY":"蜂场id"}]}
*/
SELECT b.create_time AS '合作时间',
       sum(b.number) AS '发放数量/箱',
       ba.`name`     AS '蜂友姓名',
       ba.phone      AS '蜂友电话',
       b.creator_id  AS '操作人',
       b.apiary_id   AS '蜂场id'
FROM `mp-asset`.t_asset_ledger_batch b,
     `mp-asset`.t_user_base ba
WHERE TO_DAYS(b.create_time) = TO_DAYS(NOW())
  AND b.cur_owner_id = ba.user_id
  AND b.cur_owner_type = 3
  AND b.type = 30
  AND b.is_delete = 0
  AND ba.is_delete = 0
GROUP BY b.cur_owner_id;

/*
{"email_title":"资产发放统计","statement_title":"历史资产发放统计","combine_label":"AssetReleaseStatisticsAll","combine":False,"combine_key":None,"LORD_VICE_MERGE":True,"VICE_MERGE":False,"DBname":"mp","DBstatus":True,"DBlist":[{"DBname":"flower","sqlfile":"creator_name.sql","db_key":[{"Value":"操作人","replace":"操作人list"}],"MERGE_KEY":"操作人"},{"DBname":"flower","sqlfile":"asset_release_apiary_info.sql","db_key":[{"Value":"蜂场id","replace":"swarmid"}],"MERGE_KEY":"蜂场id"}]}
*/
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