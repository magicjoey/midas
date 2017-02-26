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
import datetime
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


def get_direction(trade_type, is_second=False):
    if trade_type in ['payout']:
        return "O"
    elif trade_type in ['income', 'reimburse', 'receivables','bonus']:
        return "I"
    elif trade_type in ['transfer', 'invest', 'cashback']:
        if is_second:
            return "I"
        else:
            return "O"
    raise ValueError("交易类型错误")


def calc_after_amount(accounting_type, before_amount, amount, is_second=False):
    direction = get_direction(accounting_type, is_second)
    if direction == "O":
        return before_amount-amount
    elif direction == "I":
        return before_amount+amount
    # elif direction == "T":
    #     if is_second:
    #         return "I"
    #     else:
    #         return "O"


def get_date(days=0):
    return datetime.date.today() + datetime.timedelta(days=days)


def get_today():
    return get_date()


def get_yesterday():
    return get_date(-1)


def get_tomorrow():
    return get_date(1)


if __name__ == '__main__':
    print(get_yesterday())