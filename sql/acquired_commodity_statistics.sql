/*
{"email_title":"追花族每日收购商品统计","statement_title":"每日收购商品统计","combine_label":"add_up_statistics","combine":False,"combine_key":None}
*/
SELECT purchase_date                                AS '收购日期',
       r.real_name                                  AS '蜂友姓名',
       co.value                                     AS '纯度',
       humidity                                     AS '湿度',
       rr.real_name                                 AS '收购人姓名',
       CONCAT(re.full_name, ra.full_name,
              rb.full_name)                         AS '产地',
       s.hive_num                                   AS '合作蜂群数',
       p.weight                                     AS '重量KG',
       cast(weight / s.hive_num AS decimal(18, 2))  AS '单箱产量',
       cast(p.total_amount / 100 AS decimal(18, 2)) AS '收购金额(元)',
       cast(p.price / 100 AS decimal(18, 2))        AS '单价(元/KG)'
FROM `fc-trade`.t_product p,
     `fc-bee`.t_bee_friend r,
     `fc-bee`.t_bee_friend rr,
     `fc-bee`.t_region re,
     `fc-bee`.t_region ra,
     `fc-bee`.t_region rb,
     `fc-bee`.t_swarm_info s,
     `fc-trade`.t_purchase_order por,
     `fc-bee`.t_config co
WHERE TO_DAYS(purchase_date) = TO_DAYS(NOW())
  AND p.seller_id = r.user_id
  AND p.creator_id = rr.user_id
  AND re.id = p.province
  AND ra.id = p.city
  AND rb.id = p.county
  AND s.id = por.swarm_id
  AND por.order_no = p.order_no
  AND co.`key` = p.purity
ORDER BY r.user_id DESC;