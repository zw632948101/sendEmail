#### flowerSendEmail 文件使用方法
+ 使用改文件直接写在flowerSQL.sql文件中写sql和备注，通过读取sql备注对sql返回数据进行拼装
#### flowerSQL.sql写sql规范
+ 注意：如果不按照规划编写，程序将不能执行，每条备注和sql一一对应，需要严格按照规范编写<br />
1.备注写法<br />
 ```
/*
{"email_title":"资产发放统计","statement_title":"每日资产发放统计","combine_label":"AssetReleaseStatistics","combine":False,"combine_key":None,"DBname":"mp","DBstatus":True,"DBlist":[{"DBname":"flower","sqlfile":"creator_name.sql","db_key":"操作人","replace":"creator_id"}]}
*/
 ```
+ email_title：发送邮件的标题 
+ statement_title：统计表的标题
+ combine_label：需要合并数据的标签，combine为True时将对相同标签的数据进行合并，注意同一个combine_label的combine_key必须相同
+ combine：是否需要对返回数据进行合并，False不合并，True合并
+ combine_key：合并数据使用的字段，如果数据需要合并但没有统一的key时combine_key值写为None
+ DBname: 需要重新连接的数据库名称（flower：追花族，mp：中台，worldfarm：世界农场，base：基础数据如用户数据，agrrobot：硬件智能设备项目）
+ DBstatus: 是否需要跨库查询True or False
+ DBlist: 需要跨库查询的配置
> + DBlist.DBname 需要重新连接的数据库名称，同上
> + DBlist.sqlfile 跨库查询的SQL语句
> + db_key 合并字段，跨库时与主表合并使用
> + replace 以主表合并字段db_key的值转成元祖替换在SQL中的replace值组成查询语句
+ 注意：备注里面不能有(;)如果有分号程序将报错
2.sql写法
+ sql结尾时才能写分号且每条sql必须带分号结尾 
3.跨库查询时区分主表与附表，附表查询语句放置substatements文件下