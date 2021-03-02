SELECT tbf.user_id,tbf.real_name AS '创建人'
FROM `fc-bee`.t_bee_friend tbf WHERE tbf.is_delete = 0 AND tbf.user_id IN userid;