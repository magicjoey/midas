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
from rest import views

urlpatterns = [
    url(r'^platforms/', views.platforms),
    url(r'^login/', views.login),
    url(r'^register/', views.register),
    url(r'^invests/', views.invests),
    url(r'^reminders/', views.reminders),
]
