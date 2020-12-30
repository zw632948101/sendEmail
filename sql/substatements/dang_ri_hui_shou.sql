SELECT ra3.`name`              AS '蜂友',
       ra3.address             AS '蜂场位置',
       ra3.recover_number      AS '回收箱数(包含空箱及带蜜的)',
       ra3.recover_quanfenggai AS '全封盖(封盖率>90)箱数',
       ra3.recover_banfenggai  AS '半封盖(封盖率<90)箱数',
       ra3.recover_kong        AS '空箱数',
       rf3.mizhong             AS '回收蜜重'
FROM (SELECT ra2.*, rf2.*
      FROM (SELECT ra1.*, rf1.*
            FROM (SELECT ra.*, rf.*
                  FROM (SELECT u.`name`, a.address, count(l.id) AS recover_number, a.last_owner_id
                        FROM `mp-asset`.t_asset_ledger_batch a,
                             `mp-asset`.t_user_base u,
                             `mp-asset`.t_asset_ledger l
                        WHERE a.type = 30
                          AND a.cur_owner_type = 2
                          AND a.last_owner_type = 3
                          AND u.user_id = a.last_owner_id
                          AND a.is_delete = 0
                          AND l.is_delete = 0
                          AND l.ledger_batch_id = a.id
                          AND TO_DAYS(a.create_time) = TO_DAYS(NOW())
                        GROUP BY a.last_owner_id) ra
                           LEFT OUTER JOIN
                       (SELECT sum(number) AS recover_quanfenggai, last_owner_id AS last_id
                        FROM `mp-asset`.t_asset_ledger_batch
                        WHERE relation_no IN relation_no_list1
                            AND is_delete = 0
                            AND TO_DAYS(create_time) = TO_DAYS(NOW())
                        GROUP BY last_owner_id) rf
                       ON ra.last_owner_id = rf.last_id) ra1
                     LEFT OUTER JOIN
                 (SELECT sum(number) AS recover_banfenggai, last_owner_id AS ban_id
                  FROM `mp-asset`.t_asset_ledger_batch
                  WHERE relation_no IN relation_no_list2
                      AND is_delete = 0
                      AND TO_DAYS(create_time) = TO_DAYS(NOW())
                  GROUP BY last_owner_id) rf1
                 ON rf1.ban_id = ra1.last_owner_id) ra2
               LEFT OUTER JOIN
           (SELECT last_owner_id AS id_kong, sum(number) AS recover_kong
            FROM `mp-asset`.t_asset_ledger_batch
            WHERE relation_no IS NULL
              AND is_delete = 0
              AND TO_DAYS(create_time) = TO_DAYS(NOW())
            GROUP BY last_owner_id) rf2
           ON rf2.id_kong = ra2.last_owner_id) ra3
         LEFT OUTER JOIN
     (SELECT last_owner_id, (sum(le.weight) - sum(le.last_weight)) / 1000 AS mizhong
      FROM `mp-asset`.t_asset_ledger_batch bat,
           `mp-asset`.t_asset_ledger le
      WHERE bat.relation_no IS NOT NULL
        AND bat.type = 30
        AND bat.cur_owner_type = 2
        AND bat.last_owner_type = 3
        AND bat.is_delete = 0
        AND le.is_delete = 0
        AND le.ledger_batch_id = bat.id
        AND TO_DAYS(bat.create_time) = TO_DAYS(NOW())
      GROUP BY last_owner_id) rf3
     ON rf3.last_owner_id = ra3.last_owner_id;