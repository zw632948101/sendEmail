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