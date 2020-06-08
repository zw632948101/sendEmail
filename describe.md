#### flowerSendEmail 文件使用方法
>使用改文件直接写在flowerSQL.sql文件中写sql和备注，通过读取sql备注对sql返回数据进行拼装
#### flowerSQL.sql写sql规范
>注意：如果不按照规划编写，程序将不能执行，每条备注和sql一一对应，需要严格按照规范编写
>1.备注写法
/*
{"email_title":"测试报表","statement_title":"采集蜂场统计报表","combine_label":"test2","combine":False,"combine_key":"联系方式"}
*/
email_title：发送邮件的标题 
statement_title：统计表的标题
combine_label：需要合并数据的标签，combine为True时将对相同标签的数据进行合并，注意同一个combine_label的combine_key必须相同
combine：是否需要对返回数据进行合并，False不合并，True合并
combine_key：合并数据使用的字段，如果数据需要合并但没有统一的key时combine_key值写为None
注意：备注里面不能有(;)如果有分号程序将报错
>2.sql写法
sql结尾时才能写分号且每条sql必须带分号结尾 