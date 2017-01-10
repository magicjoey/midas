#!/usr/bin/env python
# encoding: utf-8
"""
    @author: Magic Joey
    @contact: outlierw@gmail.com
    @site: http://underestimated.me
    @project: eyoo_service
    @description:
    @version: 2016-10-07 00:02,api_util V1.0 
"""
from rest_framework import status
from rest_framework.response import Response


@staticmethod
def build_response(data, sta):
    data_dict = {}
    if data is not None and type(data) == type(dict) and data.index('code')>-1:
        data_dict = data
    else:
        if sta is not None and (
        status.HTTP_200_OK, status.HTTP_201_CREATED, status.HTTP_202_ACCEPTED, status.HTTP_304_NOT_MODIFIED).index(
                sta) > -1:
            data_dict['code'] = "S"
        else:
            data_dict['code'] = "F"
        if data is not None and type(data) == type(dict) and data.length == 1:
            data_dict['msg'] = data[0].value()
        else:
            if data_dict['code'] == "S":
                data_dict['msg'] = "请求成功"
            else:
                data_dict['msg'] = "请求失败"
    return Response(data_dict, status=sta)
