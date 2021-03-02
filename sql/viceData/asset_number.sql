SELECT product_no
FROM `fc-trade`.t_product
WHERE IFNULL(cap_rate, 0) >= 90
  AND is_delete = 0;
SELECT product_no AS product_no1
FROM `fc-trade`.t_product
WHERE IFNULL(cap_rate, 0) < 90
  AND is_delete = 0;