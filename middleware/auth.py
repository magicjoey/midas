#!/usr/bin/env python
# encoding: utf-8
"""
    @author: Magic Joey
    @contact: outlierw@gmail.com
    @site: http://underestimated.me
    @project: midas
    @description:
    @version: 2017-01-29 10:19,logincheck V1.0 
"""
from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.response import Response

need_not_login_urls = ['/api/login/', '/api/logout/', '/api/register', '/api/recover/', '/login/', '/register/','/recover/', '/static/']


class AuthCheckMiddleware(object):

    def process_request(self, request):
        url = request.path
        for single_nlurl in need_not_login_urls:
            if url.find(single_nlurl) == 0:
                return None
        try:
            assert request.session['login_user'] is not None, "登陆用户不可为空"
        except Exception as e:
            if url.find("/api/") == 0:
                return Response({"code": "F", "msg": e}, status=status.HTTP_200_OK)
            else:
                return HttpResponseRedirect("/login/")
        return None

    def process_response(self, request, response):
        return response