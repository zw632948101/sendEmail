-- 资产发放统计 - 操作人查询
SELECT tb.user_id AS '操作人', tb.real_name AS '操作人姓名'
FROM `fc-bee`.t_bee_friend tb
WHERE tb.user_id IN 操作人list;