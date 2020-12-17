#### flowerSendEmail 文件使用方法
+ 使用改文件直接写在flowerSQL.sql文件中写sql和备注，通过读取sql备注对sql返回数据进行拼装
#### flowerSQL.sql写sql规范
+ 注意：如果不按照规划编写，程序将不能执行，每条备注和sql一一对应，需要严格按照规范编写<br />
1.备注写法<br />
 ```
/*
{
    "email_title":"资产回收统计",
    "statement_title":"浅继箱业务汇总",
    "combine_label":"test",
    "combine":"False",
    "combine_key":None,
    "LORD_VICE_MERGE":False,
    "VICE_MERGE":True,
    "DBname":"flower",
    "DBstatus":True,
    "DBlist":[
        {
            "DBname":"mp",
            "sqlfile":"hui_shou_hui_zong.sql",
            "db_key":[
                {
                    "Value":"product_no",
                    "replace":"relation_no_list1"
                },
                {
                    "Value":"product_no1",
                    "replace":"relation_no_list2"
                }
            ],
            "MERGE_KEY":"user_id"
        },
        {
            "DBname":"flower",
            "sqlfile":"shallow_check.sql",
            "db_key":[

            ],
            "MERGE_KEY":"user_id"
        }
    ]
}
*/
 ```
+ email_title：发送邮件的标题 
+ statement_title：统计表的标题
+ combine_label：(已遗弃)需要合并数据的标签，combine为True时将对相同标签的数据进行合并，注意同一个combine_label的combine_key必须相同
+ combine：是否需要对返回数据进行合并，False不合并，True合并
+ combine_key：合并数据使用的字段，如果数据需要合并但没有统一的key时combine_key值写为None
+ DBname: 需要重新连接的数据库名称（flower：追花族，mp：中台，worldfarm：世界农场，base：基础数据如用户数据，agrrobot：硬件智能设备项目）
+ DBstatus: 是否需要跨库查询True or False
+ LORD_VICE_MERGE: 主表与副表合并，合并字段以MERGE_KEY相同进行合并
+ VICE_MERGE: 副表合并，并且舍弃主表数据，合并字段以MERGE_KEY相同进行合并
+ DBlist: 需要跨库查询的配置
> + DBlist.DBname 需要重新连接的数据库名称，同上
> + DBlist.sqlfile 跨库查询的SQL语句
> + db_key 取值替换字段[{"Value":"取值字段","replace":"替换字段"},...]
> + MERGE_KEY 合并字段以第一个表为主表进行合并，暂时只能支持两个表合并
+ 注意：备注里面不能有(;)如果有分号程序将报错
2.sql写法
+ sql结尾时才能写分号且每条sql必须带分号结尾 
3.跨库查询时区分主表与附表，附表查询语句放置substatements文件下