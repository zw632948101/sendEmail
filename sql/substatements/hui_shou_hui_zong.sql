SELECT GrantSum.`name`                                                       AS '蜂友姓名',
       GrantSum.address                                                      AS '蜂场位置',
       GrantSum.number_all_fa                                                AS '发放箱数',
       (GrantSum.number_all_fa - IFNULL(recover_sum.all_number_recovery, 0)) AS '待回收箱数',
       IFNULL(recover_sum.all_number_recovery, 0)                            AS '已回收箱数(包含空箱及带蜜)',
       IFNULL(recover_sum.recover_quanfenggai, 0)                            AS '全封盖(封盖率>=90)箱数',
       IFNULL(recover_sum.recover_banfenggai, 0)                             AS '半封盖(封盖率<90)箱数',
       IFNULL(recover_sum.recover_kong, 0)                                   AS '空箱数',
       GrantSum.cur_owner_id as user_id
FROM (SELECT bu.`name`, b.address, sum(b.number) AS number_all_fa, b.cur_owner_id
      FROM `mp-asset`.t_asset_ledger_batch b,
           `mp-asset`.t_user_base bu
      WHERE b.cur_owner_id = bu.user_id
        AND b.cur_owner_type = 3
        AND b.type = 30
        AND b.last_owner_type = 2
        AND b.is_delete = 0
      GROUP BY b.cur_owner_id) GrantSum
         LEFT OUTER JOIN
     (SELECT cover.*, Kcover.recover_kong
      FROM (SELECT cv1.last_owner_id,
                   cv1.all_number_recovery,
                   cv1.recover_quanfenggai,
                   cp1.recover_banfenggai
            FROM (SELECT cv.*, cp.*
                  FROM (SELECT bb.last_owner_id, count(l.id) AS all_number_recovery
                        FROM `mp-asset`.t_asset_ledger_batch bb,
                             `mp-asset`.t_asset_ledger l
                        WHERE bb.type = 30
                          AND bb.cur_owner_type = 2
                          AND bb.last_owner_type = 3
                          AND bb.is_delete = 0
                          AND bb.id = l.ledger_batch_id
                          AND l.is_delete = 0
                        GROUP BY bb.last_owner_id) cv
                           LEFT OUTER JOIN
                       (SELECT sum(number) AS recover_quanfenggai, last_owner_id AS last_id
                        FROM `mp-asset`.t_asset_ledger_batch
                        WHERE relation_no IN
                              relation_no_list1
                          AND is_delete = 0
                        GROUP BY last_owner_id) cp
                       ON cp.last_id = cv.last_owner_id) cv1
                     LEFT OUTER JOIN
                 (SELECT sum(number) AS recover_banfenggai, last_owner_id
                  FROM `mp-asset`.t_asset_ledger_batch
                  WHERE relation_no IN
                        relation_no_list2
                    AND is_delete = 0
                  GROUP BY last_owner_id) cp1
                 ON cp1.last_owner_id = cv1.last_owner_id) cover
               LEFT OUTER JOIN
           (SELECT last_owner_id AS id_kong, sum(number) AS recover_kong
            FROM `mp-asset`.t_asset_ledger_batch
            WHERE relation_no IS NULL
              AND is_delete = 0
            GROUP BY last_owner_id) Kcover
           ON Kcover.id_kong = cover.last_owner_id) recover_sum
     ON recover_sum.last_owner_id = GrantSum.cur_owner_id;