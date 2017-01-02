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
from api.models import Platform


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

