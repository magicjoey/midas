#!/usr/bin/env python
# encoding: utf-8
"""
    @author: Magic Joey
    @contact: outlierw@gmail.com
    @site: http://underestimated.me
    @project: midas
    @description:
    @version: 2017-01-08 15:58,account_views V1.0 
"""
from rest_framework.decorators import api_view
from api.models import User
from api.serialzers import LoginSerializer, AccountSerializer


@api_view(['POST'])
def add_account(request):
    """
    增加账户接口
    ---
    request_serializer: AccountSerializer
    """
    serializer = AccountSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user = request.session['login_user']
            serializer.save(user_id=user.id)
        except User.DoesNotExist:
            return Response({"code": "F", "msg": "无此用户"}, status=status.HTTP_404_NOT_FOUND)
        except AssertionError as e:
            return Response({"code": "F", "msg": e}, status=status.HTTP_406_NOT_ACCEPTABLE)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
