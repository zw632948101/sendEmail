SELECT user_id, count(id) AS '已安装数量'
FROM `fc-bee`.t_shallow_check
WHERE is_delete = 0
GROUP BY user_id;