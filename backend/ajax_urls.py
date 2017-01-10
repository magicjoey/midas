#!/usr/bin/env python
# encoding: utf-8
"""
    @author: Magic Joey
    @contact: outlierw@gmail.com
    @site: http://underestimated.me
    @project: midas
    @description:
    @version: 2017-01-08 15:31,ajax_urls V1.0 
"""
from django.conf.urls import url, include
from backend import ajax_views

urlpatterns = [
    url(r'add_acct/', ajax_views.add_account),
    url(r'add_acct_type/', ajax_views.add_account_type),
    ]