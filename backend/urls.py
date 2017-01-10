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
    url(r'finance/', views.finance),
    url(r'donate/', views.donate),
    url(r'profile/', views.profile),
    url(r'password/', views.password),
    url(r'ajax/', include("backend.ajax_urls"))
    ]