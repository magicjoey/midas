from datetime import datetime, timedelta
import json
import random
from string import Template
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from api.models import Platform, User, SmsRecord, SmsTemplate, Config, AccountType, PlatformProduct, Account, \
    AccountSub, \
    AccountFlow
from api.serialzers import PlatformSerializer, UserSerializer, RegisterSerializer, LoginSerializer, \
    LoginResponseSerializer, SmsRequestSerializer, SmsTemplateSerializer, ConfigSerializer, AccountSerializer, \
    AccountTypeSerializer, PlatformProductSerializer, AccountSubSerializer, AccountDepositSerializer, \
    AccountingSerializer, AccountFlowSerializer
import meta


@api_view(['POST'])
def register(request):
    """
    注册接口
    ---
    request_serializer: RegisterSerializer
    """
    serializer = RegisterSerializer(data=request.data)  # , many=True)
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


@api_view(['GET', 'POST'])
def account(request, format=None):
    """
    账户更新接口:
    ---
    request_serializer: AccountSerializer
    """
    param_dict = meta.to_dict(request.data)
    param_dict['user_id'] = meta.get_user_id(request)
    serializer = AccountSerializer(data=param_dict)
    if serializer.is_valid():
        serializer.save()
        # if request.data['is_deposit'] == "Y":
        # account = Account.objects.get(user_id=meta.get_user_id(request), account_type_id=param_dict['account_type'])
        # param_dict['account_id'] = account.account_id
        # dp_serializer = AccountDepositSerializer(data=param_dict)
        # if dp_serializer.is_valid():
        #     dp_serializer.save()
        # else:
        # return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        return Response({"code": "S", "msg": "更新成功"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def account_sub(request, format=None):
    """
    子账户更新接口:
    ---
    request_serializer: AccountSubSerializer
    """
    account = Account.objects.get(user_id=meta.get_user_id(request), account_id=request.data['account_id'])
    param_dict = meta.to_dict(request.data)
    param_dict['user_id'] = meta.get_user_id(request)
    serializer = AccountSubSerializer(data=param_dict)
    if serializer.is_valid():
        serializer.save()
        account.balance += serializer.data['balance']
        account.save()
        if request.POST.get('is_deposit') == "Y":
            account_sub_list = AccountSub.objects.filter(user_id=meta.get_user_id(request),
                                                         account_id=param_dict['account_id']).order_by("-gmt_create")
            param_dict['sub_id'] = account_sub_list[0].id
            dp_serializer = AccountDepositSerializer(data=param_dict)
            if dp_serializer.is_valid():
                dp_serializer.save()
            else:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        return Response({"code": "S", "msg": "更新成功"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
def platform(request):
    """
    平台更新接口:
    ---
    request_serializer: PlatformSerializer
    """
    pf_dict = meta.to_dict(request.data)
    pf_dict['owner_id'] = meta.get_user_id(request)
    serializer = PlatformSerializer(data=pf_dict)
    if serializer.is_valid():
        serializer.save()
        platform_list = meta.to_json(Platform.objects.filter(owner_id__in=[-1, meta.get_user_id(request)]))
        return Response({"code": "S", "msg": "更新成功", "platform_list": platform_list}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
def platform_product(request):
    """
    平台产品更新接口:
    ---
    request_serializer: PlatformSerializer
    """
    # pf_dict = meta.to_dict(request.data)
    # pf_dict['owner_id'] = meta.get_user_id(request)
    serializer = PlatformProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        platform_product_list = meta.to_json(PlatformProduct.objects.filter(platform_id=request.data['platform_id']))
        return Response({"code": "S", "msg": "更新成功", "platform_product_list": platform_product_list},
                        status=status.HTTP_200_OK)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
def acct_type(request):
    """
    平台类型新增接口:
    ---
    request_serializer: AccountTypeSerializer
    """
    if request.method == "POST":
        serializer = AccountTypeSerializer(data={"name": request.data['name'], "owner_id": meta.get_user_id(request)})
        if serializer.is_valid():
            serializer.save()
            acct_types = meta.to_json(AccountType.objects.filter(owner_id__in=[-1, meta.get_user_id(request)]))
            return Response({"code": "S", "msg": "更新成功", "account_types": acct_types}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        id = request.GET['id']
        try:
            account_type = AccountType.objects.get(owner_id=meta.get_user_id(request), id=id)
            account_type.delete()
        except AccountType.DoesNotExist:
            return Response({"code": "F", "msg": "删除失败"}, status.HTTP_400_BAD_REQUEST)
        acct_types = meta.to_json(AccountType.objects.filter(owner_id__in=[-1, meta.get_user_id(request)]))
        return Response({"code": "S", "msg": "更新成功", "account_types": acct_types}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', "DELETE"])
def accounting(request):
    """
    通用记账接口：
    ---
    request_serializer: AccountingSerializer
    """
    if request.method == "POST":
        # 判断待收款账户类型是否存在
        serializer = AccountingSerializer(data=request.data)
        if serializer.is_valid():
            income_account = None
            if serializer.data['accounting_type'] in ["receivables"]:
                try:
                    raw_sql = "select * from tb_account ac where ac.user_id=%s and exists(select 1 from tb_account_type a where a.id=ac.account_type and a.type=%s)"
                    account_list = Account.objects.raw(raw_sql,
                                                       [meta.get_user_id(request), serializer.data['accounting_type']])
                    assert len(list(account_list)) != 0, "账户不能为空"
                    account = account_list[0]
                except AssertionError:
                    # 新建账户
                    account_type = AccountType.objects.get(type=serializer.data['accounting_type'], owner_id=-1)
                    account = Account(account_name=account_type.name, user_id=meta.get_user_id(request),
                                      platform_id=serializer.data['platform'],
                                      account_type_id=account_type.id, balance=0, usage=account_type.name,
                                      gmt_start=datetime.now(),
                                      memo=account_type.name)
                    account.save()
            elif serializer.data['accounting_type'] in ["payout", "income"]:
                account = Account.objects.get(account_id=serializer.data['account'], user_id=meta.get_user_id(request))
            elif serializer.data['accounting_type'] in ["transfer"]:
                account = Account.objects.get(account_id=serializer.data['account'], user_id=meta.get_user_id(request))
                income_account = Account.objects.get(account_id=serializer.data['income_account'],
                                                     user_id=meta.get_user_id(request))
            flow_serial = AccountFlowSerializer(
                __accounting(serializer, account, meta.get_user_id(request), income_account))
            return Response({"code": "S", "msg": "保存成功", "flow": flow_serial.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


def __accounting(accounting, account, user_id, income_account=None):
    after_balance = meta.calc_after_amount(accounting.data['accounting_type'], account.balance,
                                           accounting.data['amount'], False)
    flow = AccountFlow(user_id=user_id, account_id_id=account.account_id, amount=accounting.data['amount'],
                       before_balance=account.balance,
                       after_balance=after_balance,
                       operate_type=accounting.data['accounting_type'],
                       direction=meta.get_direction(accounting.data['accounting_type'], False),
                       memo=accounting.data['memo'],
                       label=accounting.data['label'])
    account.balance = after_balance
    account.gmt_modified = timezone.now()
    account.save()
    flow.save()

    #转账的收款账户
    if accounting.data['accounting_type'] in ["transfer"] and income_account is not None:
        after_balance2 = meta.calc_after_amount(accounting.data['accounting_type'], income_account.balance,
                                                accounting.data['amount'], True)
        flow2 = AccountFlow(user_id=user_id, account_id_id=income_account.account_id, amount=accounting.data['amount'],
                            before_balance=income_account.balance,
                            after_balance=after_balance2,
                            operate_type=accounting.data['accounting_type'],
                            direction=meta.get_direction(accounting.data['accounting_type'], True),
                            memo=accounting.data['memo'],
                            label=accounting.data['label'])
        income_account.balance = after_balance2
        income_account.gmt_modified = timezone.now()
        income_account.save()
        flow2.save()

    return flow
