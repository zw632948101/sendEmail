-- 资产发放统计 - 蜂场位置查询
SELECT ts.id                                                                      AS '蜂场id',
       concat((SELECT tr.name FROM `fc-bee`.t_region tr WHERE tr.id = ts.province), '/',
              (SELECT tr.name FROM `fc-bee`.t_region tr WHERE tr.id = ts.city), '/',
              (SELECT tr.name FROM `fc-bee`.t_region tr WHERE tr.id = ts.county)) AS '蜂场位置'
FROM `fc-bee`.t_swarm_info ts
WHERE ts.id IN swarmid;