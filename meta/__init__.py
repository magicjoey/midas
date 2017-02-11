#!/usr/bin/env python
# encoding: utf-8
"""
    @author: Magic Joey
    @contact: outlierw@gmail.com
    @site: http://underestimated.me
    @project: midas
    @description:
    @version: 2017-01-30 11:10,__init__ V1.0 
"""
import json
from django.core import serializers


def to_json(query_set):
    data = serializers.serialize("json", query_set)
    res = []
    if data is None or len(data) == 0:
        return res
    for single in json.loads(data):
        fields = single['fields']
        fields['pk'] = single['pk']
        res.append(fields)
    return res


def to_dict(query_dict):
    return query_dict.dict()


def get_user_id(request):
    return request.session['login_user'].get("id")
