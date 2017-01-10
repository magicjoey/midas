from datetime import datetime, timedelta
import json
import random
from string import Template
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from api.models import Platform, User, SmsRecord, SmsTemplate, Config
from api.serialzers import PlatformSerializer, UserSerializer, RegisterSerializer, LoginSerializer, \
    LoginResponseSerializer, SmsRequestSerializer, SmsTemplateSerializer, ConfigSerializer
from api.throttle import SmsRateThrottle
from api.util import build_response


@api_view(['POST'])
def register(request):
    """
    注册接口
    ---
    request_serializer: RegisterSerializer
    """
    serializer = RegisterSerializer(data=request.data)#, many=True)
    if serializer.is_valid():
        try:
            # 校验短信验证码
            half_hour = datetime.now() - timedelta(seconds=1800)
            sms_records = SmsRecord.objects.filter(mobile_no=serializer.data['mobile_no'], type='register',
                                                   gmt_create__gte=half_hour).order_by('-gmt_create')
            assert len(sms_records) != 0 and sms_records[0].verify_code == serializer.data['sms_code'], "短信验证码不正确"
            password = make_password(serializer.data['password'], '', 'pbkdf2_sha256')
            user = User(user_name=serializer.data['mobile_no'], role='USER', password=password,
                        gmt_create=datetime.now())
            user.save()
        except SmsRecord.DoesNotExist:
            return Response({"code": "F", "msg": "请重新申请短信验证码"})
        except AssertionError as e:
            return Response({"code": "F", "msg": str(e)})
        return Response({"code": "S", "msg": "注册成功"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    # return build_response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    """
    登陆接口
    ---
    request_serializer: LoginSerializer
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user = User.objects.get(user_name=serializer.data['mobile_no'])
            assert check_password(serializer.data['password'], user.password, '', 'pbkdf2_sha256'), "用户名密码不正确"
            login_response = LoginResponseSerializer(user)
            # 设置 session
            request.session['login_user'] = login_response.data
            return Response({"code": "S", "user": login_response.data}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"code": "F", "msg": "无此用户"}, status=status.HTTP_404_NOT_FOUND)
        except AssertionError as e:
            return Response({"code": "F", "msg": e}, status=status.HTTP_406_NOT_ACCEPTABLE)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
def profile(request):
    pass


@api_view(['POST'])
# @throttle_classes([SmsRateThrottle])
def sms(request):
    """
    短信发送接口:（正式环境不会返回短信验证码）
    ---
    request_serializer: SmsRequestSerializer
    """
    serializer = SmsRequestSerializer(data=request.data)

    if serializer.is_valid():
        code = random.randint(100000, 999999)
        arr = {"verifyCode": code}
        try:
            smsTemplate = SmsTemplate.objects.get(type=serializer.data['type'])
            template_serial = SmsTemplateSerializer(smsTemplate, many=False)
        except SmsTemplate.DoesNotExist:
            return Response({"code": "F", "msg": "短信模板未配置"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            sms_config = Config.objects.get(name="sms_config")
            config_serial = ConfigSerializer(sms_config, many=False)
            config_json = json.loads(config_serial.data['content'])
        except Config.DoesNotExist:
            return Response({"code": "F", "msg": "短信配置为空"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except (ValueError, KeyError, TypeError):
            return Response({"code": "F", "msg": "短信配置解析出错"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        content = Template(template_serial.data['content']).substitute(arr)
        # 短信发送记录
        SmsRecord(mobile_no=serializer.data['mobile_no'], content=content, verify_code=code,
                  type=serializer.data['type'],
                  gmt_create=datetime.now()).save()
        # result = sms_client.send_lsm(serializer.data['mobile_no'], content, config_json['url'], config_json['api'])
        # logger.log(result)
        # TODO:返回结果吗仍需要处理
        return Response({"code": "S", "msg": "短信发送成功", "sms_code": code}, status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def calendar(request, format=None):
    pts = Platform.objects.all()
    serializer = PlatformSerializer(pts, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def platforms(request, format=None):
    user_id = request.GET.get("user_id")
    pts = Platform.objects.filter(owner_type='system')
    pts_user = Platform.objects.filter(owner_type='user')
    serializer = PlatformSerializer(pts, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def platform_add(request, format=None):
    pts = Platform.objects.all()
    serializer = PlatformSerializer(pts, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def platform_delete(request, format=None):
    pts = Platform.objects.all()
    serializer = PlatformSerializer(pts, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def products(request, format=None):
    pts = Platform.objects.all()
    serializer = PlatformSerializer(pts, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def product_add(request, format=None):
    pts = Platform.objects.all()
    serializer = PlatformSerializer(pts, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def product_delete(request, format=None):
    pts = Platform.objects.all()
    serializer = PlatformSerializer(pts, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def invest_add(request, format=None):
    pass

@api_view(['GET', 'POST'])
def invest_delete(request, format=None):
    pass

@api_view(['GET', 'POST'])
def invests(request, format=None):
    pass


@api_view(['GET', 'POST'])
def reminders(request, format=None):
    pass
