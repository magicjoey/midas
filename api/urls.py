#!/usr/bin/env python
# encoding: utf-8
"""
    @author: Magic Joey
    @contact: outlierw@gmail.com
    @site: http://underestimated.me
    @project: midas
    @description:
    @version: 2016-06-22 20:10,urls V1.0 
"""
from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^platform/', views.platform),
    url(r'^platform_product/', views.platform_product),
    url(r'^login/', views.login),
    url(r'^register/', views.register),
    url(r'^invests/', views.invests),
    url(r'^reminders/', views.reminders),
    url(r'^sms/', views.sms),
    url(r'^account/', views.account),
    url(r'^account_sub/', views.account_sub),
    url(r'^acct_type/', views.acct_type),
    url(r'^accounting/', views.accounting),

]
