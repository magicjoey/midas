#!/usr/bin/env python
# encoding: utf-8
"""
    @author: Magic Joey
    @contact: outlierw@gmail.com
    @site: http://underestimated.me
    @project: eyoo_service
    @description:
    @version: 2016-10-07 09:48,throttle V1.0 
"""
from rest_framework import throttling
from api.models import  RateParam
from api.serialzers import SmsRequestSerializer

"""
    30秒内1次
    5min内3次
    1天内10次
"""
class SmsRateThrottle(throttling.BaseThrottle):
    def allow_request(self, request, view):
        sms_serializer = SmsRequestSerializer(data=request.data)
        if sms_serializer.is_valid():
            sql = """select max(max_id) id,sum(if(type='half_minute',cnt,0)) AS half_second,sum(if(type='five_minutes',cnt,0)) AS five_minutes,sum(if(type='one_day',cnt,0)) AS one_day
    from(select max(id) max_id,count(1) cnt,'half_minute' type from tb_sms_record where mobile_no='15901845510' and gmt_create>DATE_SUB(NOW(),INTERVAL 30 SECOND)
     union select max(id) max_id,count(1) cnt,'five_minutes' type from tb_sms_record where mobile_no='15901845510' and gmt_create>DATE_SUB(NOW(),INTERVAL 5 MINUTE)
     union select max(id) max_id,count(1) cnt,'one_day' type from tb_sms_record where mobile_no='15901845510' and gmt_create>DATE_SUB(NOW(),INTERVAL 1 DAY)) b"""
            rate_param_list = RateParam.objects.raw(sql)
            rate_param = rate_param_list[0]
            return rate_param.half_second<=1 and rate_param.five_minutes <= 3 and rate_param.one_day <=10
        return True
