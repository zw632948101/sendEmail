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