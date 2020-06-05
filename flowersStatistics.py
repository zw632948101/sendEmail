#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
import schedule
import time
from sendEmail import sendEmail


def job():
    """
    要周期运行的函数
    """
    a = sendEmail()
    a.send_flowers_collection_statistics()
    del a

# schedule.every(10).seconds.do(job)
# schedule.every(1).minutes.do(job)               # 每隔 10 分钟运行一次 job 函数
# schedule.every().hour.do(job)                    # 每隔 1 小时运行一次 job 函数
schedule.every().day.at("20:00").do(job)         # 每天在 10:30 时间点运行 job 函数
# schedule.every().monday.do(job)                  # 每周一 运行一次 job 函数
# schedule.every().wednesday.at("13:15").do(job)   # 每周三 13：15 时间点运行 job 函数
# schedule.every().minute.at(":17").do(job)        # 每分钟的 17 秒时间点运行 job 函数

while True:
    schedule.run_pending()   # 运行所有可以运行的任务
    time.sleep(1)
