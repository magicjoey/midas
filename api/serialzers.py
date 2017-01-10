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
from api.models import Platform, User, SmsTemplate, Config


class PlatformSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    platform_name = serializers.CharField(required=True, allow_blank=False, max_length=32)
    owner_type = serializers.CharField(max_length=5)
    owner_id = serializers.IntegerField(allow_null=True)
    gmt_create = serializers.DateTimeField(allow_null=True)

    def create(self, validated_data):
        return Platform.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.platform_name = validated_data.get('platform_name', instance.platform_name)
        instance.owner_type = validated_data.get('owner_type', instance.owner_type)
        instance.owner_id = validated_data.get('owner_id', instance.owner_id)
        instance.gmt_create = validated_data.get('gmt_create', instance.gmt_create)
        instance.save()
        return instance

class UserSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    pk = serializers.IntegerField(read_only=True)
    user_name = serializers.CharField(required=True,max_length=32, allow_null=False, )
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
    nickname = serializers.CharField(required=True,max_length=16, min_length=1)
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



class AccountSerializer(CommonSerializer):
    account_name = serializers.CharField(max_length=32)
    platform = serializers.CharField(max_length=20)
    platform_id = serializers.IntegerField()
    account_type = serializers.CharField(max_length=10)
    balance = serializers.FloatField()
    usage = serializers.CharField(max_length=20)
    gmt_start = serializers.DateField()
    cycle = serializers.IntegerField()
    gmt_end = serializers.DateField()
    return_rate = serializers.FloatField()
    memo = serializers.CharField(max_length=100)
    status = serializers.CharField(max_length=1)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass