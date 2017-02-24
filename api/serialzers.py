#!/usr/bin/env python
# encoding: utf-8
"""
    @author: Magic Joey
    @contact: outlierw@gmail.com
    @site: http://underestimated.me
    @project: midas
    @description:
    @version: 2016-06-22 20:21,serialzers V1.0 
"""
from rest_framework import serializers
from api import fields
from api.models import Platform, User, SmsTemplate, Config, AccountType, Account, PlatformProduct, AccountSub, \
    AccountDeposit, AccountFlow


class PlatformSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Platform
        fields = ('platform_name', 'owner_id', 'gmt_create', 'memo')


class PlatformProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformProduct
        fields = ('platform_id', 'product_name', 'repay_type', 'interest_rate')


class UserSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    pk = serializers.IntegerField(read_only=True)
    user_name = serializers.CharField(required=True, max_length=32, allow_null=False, )
    nick_name = serializers.CharField(max_length=20)
    role = serializers.CharField(max_length=8)
    avatar = serializers.CharField(max_length=128)
    introduction = serializers.CharField(max_length=128)


class CommonSerializer(serializers.Serializer):
    # uuid = serializers.CharField(max_length=128, allow_null=False, allow_blank=False, )
    # ip_addr = serializers.CharField(max_length=32, allow_null=False, allow_blank=False, )
    # platform = serializers.ChoiceField(allow_null=False, allow_blank=False, choices=(("android", "安卓"), ("ios", "IOS"),
    #                                                                                  ("wap", "wap端")))

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class RegisterSerializer(CommonSerializer):
    mobile_no = fields.MobileField()
    nickname = serializers.CharField(required=True, max_length=16, min_length=1)
    password = serializers.CharField(required=True, max_length=32, min_length=6)
    sms_code = serializers.CharField(required=True, max_length=6, min_length=6)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class LoginSerializer(CommonSerializer):
    mobile_no = fields.MobileField()
    password = serializers.CharField(required=True, max_length=32, min_length=6)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class LoginResponseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'user_name', 'status', 'is_active', 'is_admin', 'is_delete', 'nick_name', 'role', 'avatar',
                  'introduction', 'sex', 'birthday', 'gmt_login', 'gmt_create', 'gmt_update')


class SmsRequestSerializer(CommonSerializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    mobile_no = fields.MobileField()
    type = serializers.ChoiceField(allow_null=False, allow_blank=False, choices=(("register", "注册"), ("login", "登陆"),
                                                                                 ("withdraw", "提现"),
                                                                                 ("recover", "找回密码")))


class SmsTemplateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SmsTemplate
        fields = ('type', 'content', 'gmt_create')


class ConfigSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Config
        fields = ('name', 'content', 'gmt_create', 'gmt_modified')


class AccountTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AccountType
        fields = ('name', 'owner_id', 'gmt_create')


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'account_id', 'account_name', 'user_id', 'platform', 'account_type', 'balance', 'usage', 'gmt_start',
            'cycle',
            'gmt_end', 'return_rate', 'memo')


class AccountSubSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountSub
        fields = (
            'account_id', 'account_name', 'user_id', 'product_id', 'memo', 'balance', 'return_rate', 'redeem_type',
            'gmt_start', 'gmt_end', 'status', 'gmt_create', 'gmt_modified')


class AccountDepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountDeposit
        fields = (
            'account_id', 'user_id', 'sub_id', 'account_type', 'deposit_type', 'gmt_create', 'gmt_modified', 'day',
            'amount', 'base', 'deposit_rate')


class AccountingSerializer(CommonSerializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    accounting_type = serializers.ChoiceField(allow_null=False, allow_blank=False,
                                              choices=(("payout", "支出"), ("income", "收入"),
                                                       ("transfer", "转账"),
                                                       ("reimburse", "报销"), ("invest", "投资"), ("cashback", "回款"),
                                                       ("receivables", "应收款")))
    income_account = serializers.CharField(allow_null=True, required=False)
    amount = serializers.FloatField()
    gmt_end = serializers.DateField(allow_null=True, required=False)
    gmt_occur = serializers.DateField(allow_null=True, required=False)
    memo = serializers.CharField()
    account = serializers.IntegerField(allow_null=True, required=False)
    label = serializers.CharField(allow_null=True, required=False)


class AccountFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountFlow
        fields = (
        'user_id', 'account_id', 'sub_id', 'amount', 'before_balance', 'after_balance', 'operate_type', 'direction', 'memo',
        'gmt_create', 'gmt_update', 'trade_name', 'label', 'gmt_occur')
