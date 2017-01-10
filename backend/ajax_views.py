#!/usr/bin/env python
# encoding: utf-8
"""
    @author: Magic Joey
    @contact: outlierw@gmail.com
    @site: http://underestimated.me
    @project: midas
    @description:
    @version: 2017-01-08 15:31,ajax_views V1.0 
"""
from django.shortcuts import render


def add_account(request):
    return render(request, "backend/ajax/add_account.html", {})

def add_account_type(request):
    return render(request, "backend/ajax/add_account_type.html", {})