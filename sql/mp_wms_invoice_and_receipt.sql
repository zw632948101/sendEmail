/*
{"email_title":"WMS数据汇总","statement_title":"入库通知单","combine_label":"test","combine":False,"combine_key":None,"LORD_VICE_MERGE":True,"VICE_MERGE":False,"DBname":"mp","DBstatus":True,"CONFIG_FILE":"mp_wms_document_type","CONFIG_KEY":['来源系统','单据类型'],"DBlist":[{"DBname":"flower","sqlfile":"query_username.sql","db_key":[{"Value":"user_id","replace":"userid"}],"MERGE_KEY":'user_id'}]}
*/
SELECT tr.code                                                                    AS '入库通知单',
       tr.relevance_code                                                          AS '关联单据编号',
       tr.source                                                                  AS '来源系统',
       tr.type                                                                    AS '单据类型',
       tw.name                                                                    AS '入库仓库',
       tr.creator_id                                                              AS 'user_id',
       CASE tr.status WHEN 0 THEN '待确认' WHEN 1 THEN '已确认' WHEN 2 THEN '已完成' WHEN 3 THEN '已取消' END AS '入库状态',
       tr.create_time                                                             AS '创建时间'
FROM `mp-wms`.t_whs_receipt_notice tr
         LEFT JOIN `mp-wms`.t_warehouse tw ON tr.warehouse_code = tw.code
WHERE tr.is_delete = 0
ORDER BY tr.id DESC;
/*
{"email_title":"WMS数据汇总","statement_title":"入库单","combine_label":"test","combine":False,"combine_key":None,"LORD_VICE_MERGE":True,"VICE_MERGE":False,"DBname":"mp","DBstatus":True,"CONFIG_FILE":"mp_wms_document_type","CONFIG_KEY":['来源系统','单据类型'],"DBlist":[{"DBname":"flower","sqlfile":"query_username.sql","db_key":[{"Value":"user_id","replace":"userid"}],"MERGE_KEY":'user_id'}]}
*/
SELECT tr.code                                                                    AS '入库单',
       tr.relevance_code                                                          AS '入库通知单',
       tr.source                                                                  AS '来源系统',
       tr.type                                                                    AS '单据类型',
       tw.name                                                                    AS '入库仓库',
       tr.creator_id                                                              AS 'user_id',
       CASE tr.status WHEN 0 THEN '待入库' WHEN 1 THEN '入库完成' WHEN 2 THEN '入库取消' END AS '入库状态',
       tr.create_time                                                             AS '创建时间'
FROM `mp-wms`.t_whs_receipt tr
         LEFT JOIN `mp-wms`.t_warehouse tw ON tr.warehouse_code = tw.code
WHERE tr.is_delete = 0
ORDER BY tr.id DESC;
/*
{"email_title":"WMS数据汇总","statement_title":"出库通知单","combine_label":"test","combine":False,"combine_key":None,"LORD_VICE_MERGE":True,"VICE_MERGE":False,"DBname":"mp","DBstatus":True,"CONFIG_FILE":"mp_wms_document_type","CONFIG_KEY":['来源系统','单据类型'],"DBlist":[{"DBname":"flower","sqlfile":"query_username.sql","db_key":[{"Value":"user_id","replace":"userid"}],"MERGE_KEY":'user_id'}]}
*/
SELECT tr.code                                                                    AS '出库通知单',
       tr.relevance_code                                                          AS '关联单据编号',
       tr.source                                                                  AS '来源系统',
       tr.type                                                                    AS '单据类型',
       tw.name                                                                    AS '出库仓库',
       tr.creator_id                                                              AS 'user_id',
       CASE tr.status WHEN 0 THEN '待确认' WHEN 1 THEN '已确认' WHEN 2 THEN '已完成' WHEN 3 THEN '已取消' END AS '出库状态',
       tr.create_time                                                             AS '创建时间'
FROM `mp-wms`.t_whs_invoice tr
         LEFT JOIN `mp-wms`.t_warehouse tw ON tr.warehouse_code = tw.code
WHERE tr.is_delete = 0
ORDER BY tr.id DESC;
/*
{"email_title":"WMS数据汇总","statement_title":"出库单","combine_label":"test","combine":False,"combine_key":None,"LORD_VICE_MERGE":True,"VICE_MERGE":False,"DBname":"mp","DBstatus":True,"CONFIG_FILE":"mp_wms_document_type","CONFIG_KEY":['来源系统','单据类型'],"DBlist":[{"DBname":"flower","sqlfile":"query_username.sql","db_key":[{"Value":"user_id","replace":"userid"}],"MERGE_KEY":'user_id'}]}
*/
SELECT tr.code                                                                    AS '出库单',
       tr.relevance_code                                                          AS '出库通知单',
       tr.source                                                                  AS '来源系统',
       tr.type                                                                    AS '单据类型',
       tw.name                                                                    AS '出库仓库',
       tr.creator_id                                                              AS 'user_id',
       CASE tr.status WHEN 0 THEN '待入库' WHEN 1 THEN '入库完成' WHEN 2 THEN '入库取消' END AS '出库状态',
       tr.create_time                                                             AS '创建时间'
FROM `mp-wms`.t_whs_invoice tr
         LEFT JOIN `mp-wms`.t_warehouse tw ON tr.warehouse_code = tw.code
WHERE tr.is_delete = 0
ORDER BY tr.id DESC;