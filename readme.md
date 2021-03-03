#### sendEmail 项目结构
- sendEmail
    - attachment  生成Excel文件存放路径
    - common 封装公用功能目录
    - config 执行配置存放文件
    - fileDir 存放各种路径变量
    - model  数据库模型
    - my_email 封装的发送邮件方法
    - sql   SQL相关文档存放路径
        - config SQL配置文件，对应原来SQL文件中的备注
        - dbDir 数据库存放地
        - enumerate 枚举值存放路径，在枚举没有存在数据库的时候使用，yaml文件格式
        - busuness 业务SQL文件存放路径，同一个文件如果存放多个SQL时需要注意，多条SQL必须是查询同一个数据库才行
        - viceData 业务附属数据，在跨库查询是作为业务SQL的条件使用，或者跟业务数据进行合并使用
#### flowerSQL.sql写sql规范
+ 注意：如果不按照规划编写，程序将不能执行，每条备注和sql一一对应，需要严格按照规范编写<br />
1.sql写法
+ sql结尾时才能写分号且每条sql必须带分号结尾 ";"
#### common下封装方法详解
1. config.py 作为读取配置文件的封装
2. DataAggregate.py 结果数据合并删除等操作
+ get_aggregate_result(operate_list_dict，key) 列表合并,operate_list_dict字段需要传二维列表，key作为合并字段，相同的key进行合并
+ Master_schedule_aggregate(operate_list_dict，key) 已废弃，跟上面相同，只能传两个列表进行合并
+ valueNull(dt) 删除字典中空值的key，可以是list和dict
+ data_assemble(key=None, parameters_ld=None, num=None),取字典中key相同的值，返回一个列表，parameters_ld只能是一维列表，num取值的数量
3. DataBaseOperatePool 数据库连接
+ creat_db_pool(mysql) 创建数据库连接
+ query_data(sql) 执行SQL方法
+ close_db_pool() 关闭链接
4.dataConversion 处理数据使用
+ replace_dict_value(replace_key, keep_dict, enumerate_dict) 根据入参替换值
5.dataProcessing 整个项目的核心功能，全部处理数据逻辑全部在本类中
+ initialize_parameter() 获取执行配置、邮箱服务信息、数据库账户
+ assembly_receiver_data() 获取收件人列表
+ assembly_mapping_data() 处理枚举数据替换操作
+ _merge_data() 合并数据使用
+ assembly_lord_data() 处理数据的入口，处理业务数据
+ assembly_replace_data() 处理数据，用作替换SQL中条件
+ assembly_vice_data() 处理业务附属数据使用
6. DBdataProcessing 初始化配置信息和查询配置功能
+ AssemblyConfig 该类作为初始化配置文件写入数据库使用
+ QuerySqliteData 查询数据库中配置使用
7. FileOperating 读取文件的方法封装
8. Log 日志打印封装
#### config 目录
1.config 执行配置写法
"""
initialValue: &initialValue
  SMTP_HOST: smtp.exmail.qq.com 发送邮件服务

collecting_statistics: &collecting_statistics
  QA:
    <<: *initialValue
    receiver: 接收人邮箱
      - wei.zhang@worldfarm.com
  PROD:
    <<: *initialValue
    receiver:
      - wei.zhang@worldfarm.com
  SQL_CONFIG: daily_statistics_collection SQL配置文件名称
"""
##### sql 目录
#### busuness和viceData 用作存放SQL语句文件使用
+ busuness作为业务SQL，为主要执行文件
+ viceData定位为业务复数数据，作为业务SQL的条件值出现，也可以跟业务数据进行合并
+ 注意 每条SQL结束都需要以;结尾
#### sql config SQL执行配置文件
+ 主要注意结构,参考示例
"""
EMAIL_TITLE: "邮件标题"
CONF_VERSION: 1 # 配置版本,修改SQL文件或配置文件需要向上增加,不然执行会拉取原来的配置进行查询数据
BUSUNESS: # 业务数据，列表结构，可以添加n个
  - TABLE_TITLE: "每日资产发放统计" # 表标题
    SUB_BUSUNESS:
      - MERGE: True # 是否合并 True合并 False 不合并，这里有两层用法；作为第一个出现时，只针对同一个文件中多个SQL查询数据进行合并；作为第二个时会执行两个操作，1.与第一个出现时相同，2.合并上一个出现的数据
        MERGE_KEY: '操作人' # 合并字段，如果多个SQL合并必须保证数据中都有相同的字段
        BUSUNESS_NAME: '每日资产发放统计' # 业务名称或者SQL文件的描述
        BUSUNESS_SQL_FILE: creator_name.sql # SQL文件
        BUSUNESS_VICE_MERGE: True # 是否与附属数据进行合并
        BUSUNESS_VICE_MERGE_KEY: '操作人'
        DB_NAME: "flower" # 执行查询的数据库
        BUSUNESS_MAPPING: # 替换枚举值
          - MAPPING_KEY: ['来源系统','单据类型']
            MAPPING_FILE: mp_wms_document_type # 枚举文件，yaml
        REPLACE_KEY: # 跨库查询时使用，获取附属数据进行条件值替换
          - REPLACE_VALUE: "操作人list"
            CONDITION_VALUE: "操作人"
        VICE_DATA: # 附属数据配置
          - DATA_DB_NAME: "mp"
            DATA_NAME: '每日资产发放统计-蜂友蜂场数据查询'
            DATA_SQL_FILE: daily_release_asset_bee_friend_data.sql
"""
#### 环境变量配置
MYSQL_DICT = {"数据库名称":{"MYSQL_PASSWD":"数据库密码"，"MYSQL_HOST":"数据库地址","MYSQL_PORT":"链接端口","MYSQL_USER":"账号"}}
EMAIL_SENDER = 发件人邮箱
EMAIL_PASSWD = 发件人邮箱密码
EMAIL_ENV = 环境