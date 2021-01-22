/*
{"email_title":"每日采集蜂友统计","statement_title":"每日采集蜂友统计","combine_label":"test","combine":False,"combine_key":None,"LORD_VICE_MERGE":False,"VICE_MERGE":True,"DBname":"base","DBstatus":True,"DBlist":[{"DBname":"flower","sqlfile":"statistics_friend_info_caiji.sql","db_key":[{"Value":"user_id","replace":"login_userid"}],"MERGE_KEY":'采集人'},{"DBname":"flower","sqlfile":"statistics_swarm_info_caiji.sql","db_key":[{"Value":"user_id","replace":"login_userid"}],"MERGE_KEY":'采集人'}]}
*/
SELECT tlt.user_id
FROM `world-passport`.t_login_token tlt
         LEFT JOIN `world-user`.t_user tu ON tlt.user_id = tu.id AND tu.account_type = 21
WHERE to_days(tlt.create_time) = to_days(now())
GROUP BY tlt.user_id;