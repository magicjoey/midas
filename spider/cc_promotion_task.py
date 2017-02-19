#!/usr/bin/env python
# encoding: utf-8
"""
    @author: Magic Joey
    @contact: outlierw@gmail.com
    @site: http://underestimated.me
    @project: midas
    @description: 信用卡活动获取任务
    @version: 2016-12-25 10:50,cc_promotion_task V1.0 
"""
from datetime import datetime
from pyquery import PyQuery as pyq


def crawl():
    pass


def crawl_smzdm(date=datetime.now()):
    target_url = "http://search.smzdm.com/?c=faxian&s=%E4%BF%A1%E7%94%A8%E5%8D%A1&p=1"
    doc = pyq(url=target_url, encoding="utf-8")
    activity_list = doc("#feed-main-list li.feed-row-wide")
    for activity in activity_list:
        pass

