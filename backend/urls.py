#!/usr/bin/env python
# encoding: utf-8
"""
    @author: Magic Joey
    @contact: outlierw@gmail.com
    @site: http://underestimated.me
    @project: midas
    @description:
    @version: 2017-01-02 21:37,urls V1.0 
"""
from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'login/', views.login),
    url(r'register/', views.register),
    url(r'dashboard/', views.dashboard),
    url(r'account/', views.account),
    url(r'account_sub/', views.account_sub),
    url(r'account_deposit/', views.account_deposit),
    url(r'account_type/', views.account_type),
    url(r'accounting/', views.accounting),
    url(r'account_chart/', views.account_chart),
    url(r'asset_increase/', views.asset_increase),
    url(r'lc_calendar/', views.lc_calendar),
    url(r'account/', views.account),
    url(r'finance/', views.finance),
    url(r'donate/', views.donate),
    url(r'profile/', views.profile),
    url(r'password/', views.password),
    url(r'my_cc/', views.my_cc),
    url(r'cc_list/', views.cc_list),
    url(r'cc_marketing/', views.cc_marketing),
    url(r'ajax/', include("backend.ajax_urls"))
    ]