#!/usr/bin/env python
# encoding: utf-8
"""
    @author: Magic Joey
    @contact: outlierw@gmail.com
    @site: http://underestimated.me
    @project: midas
    @description:
    @version: 2017-01-08 15:31,ajax_views V1.0 
"""
from django.shortcuts import render
from api.models import AccountType, Platform, Account, PlatformProduct
import meta


def add_account(request):
    """
    :param request:定存账户
    :return:
    """
    if "Y" == request.GET.get("is_deposit"):
        acct_type_list = AccountType.objects.filter(owner_id=-1, is_deposit='Y').order_by("owner_id", "id")
        return render(request, "backend/ajax/add_account.html",
                  {"acct_type_list": acct_type_list, "is_deposit": "Y"})
    else:
        acct_type_list = AccountType.objects.filter(owner_id__in=[-1, meta.get_user_id(request)]).order_by("owner_id", "id")
        platform_list = Platform.objects.filter(owner_id__in=[-1, meta.get_user_id(request)]).order_by("owner_id", "platform_id")
        return render(request, "backend/ajax/add_account.html",
                  {"acct_type_list": acct_type_list, "platform_list": platform_list})


def add_account_type(request):
    acct_type = AccountType.objects.filter(owner_id=-1)
    return render(request, "backend/ajax/add_account_type.html", {})

def add_platform(request):
    return render(request, "backend/ajax/add_platform.html", {})


def add_acct_sub(request):
    account = Account.objects.get(account_id=request.GET['account_id'])
    platform_product_list = PlatformProduct.objects.filter(platform_id=account.platform_id)
    return render(request, "backend/ajax/add_acct_sub.html",
                  {"account": account, "platform_product_list": platform_product_list})


def add_platform_product(request):
    platform = Platform.objects.get(platform_id=request.GET['platform_id'])
    return render(request, "backend/ajax/add_platform_product.html", {"platform":platform})