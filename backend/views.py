from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from api.models import Account, AccountType, AccountSub, AccountDeposit
import meta
from spider.bank_maintain_task import crawl


@api_view(['GET', 'POST'])
def login(request):
    """
    用户登陆
    ----------
    request_serializer:UserSerializer
    """
    if request.method == 'GET':
        code = request.GET.get('code')
        msg = request.GET.get('msg')
        return_url = request.GET.get('return_url')
        page_data = {}
        if code is not None:
            page_data['code'] = code
        if msg is not None:
            page_data['msg'] = msg
        if return_url is not None:
            page_data['returnUrl'] = return_url
        return render(request, "backend/full_page/login.html", page_data)

    return HttpResponseRedirect("/login?code=F&msg=账号不存在")


@api_view(['GET', 'POST'])
def register(request):
    if request.method == 'GET':
        code = request.GET.get('code')
        msg = request.GET.get('msg')
        role = request.GET.get("role")
        pageData = {}
        if code is not None:
            pageData['code'] = code
        if msg is not None:
            pageData['msg'] = msg
        if role is not None:
            pageData['role'] = role
        return render(request, "backend/full_page/register.html", pageData)
    return HttpResponseRedirect("/login?code=S&msg=请登录")


def dashboard(request):
    return render(request, "backend/nav_page/dashboard.html", {})


def account_chart(request):
    account_list = Account.objects.filter(user_id=meta.get_user_id(request))
    return render(request, "backend/nav_page/account_chart.html", {"account_list": account_list})


def lc_calendar(request):
    return render(request, "backend/nav_page/lc_calendar.html", {})


def account(request):
    account_list = Account.objects.filter(user_id=meta.get_user_id(request)).order_by("-account_id")
    return render(request, "backend/nav_page/account.html", {"account_list": account_list})


def accounting(request):
    return render(request, "backend/nav_page/accounting.html", {})


def account_sub(request):
    account = Account.objects.get(account_id=request.GET['account_id'])
    account_sub_list = AccountSub.objects.filter(user_id=meta.get_user_id(request),
                                                 account_id=request.GET['account_id']).order_by("-id")
    return render(request, "backend/nav_page/account_sub.html",
                  {"account_sub_list": account_sub_list, 'account': account})


def account_deposit(request):
    account_deposit_list = Account.objects.filter(user_id=meta.get_user_id(request), platform_id=-1).order_by(
        "-account_id")
    return render(request, "backend/nav_page/account_deposit.html",
                  {"account_deposit_list": account_deposit_list, 'account': account})


# 账户类型管理
def account_type(request):
    account_type_list = AccountType.objects.filter(owner_id=meta.get_user_id(request))
    return render(request, "backend/nav_page/account_type.html", {"account_type_list": account_type_list})


def finance(request):
    return render(request, "backend/nav_page/finance.html", {})


def donate(request):
    # todo 捐赠
    pass


def profile(request):
    return render(request, "backend/nav_page/profile.html", {})


def password(request):
    return render(request, "backend/nav_page/password.html", {})


def check_login(request):
    return get_login_user(request) is not None


def get_login_user(request):
    return request.session['login_user']


def asset_increase(request):
    data_dict = []
    sql = "select max(account_id) account_id,sum(balance) sum_amount from tb_account where platform!=-1"
    result = Account.objects.raw(sql)
    data_dict.append({"date": "17-1", "actual_amount": 500000, "expect_amount": 500000}
                     )
    data_dict.append({"date": "17-2", "actual_amount": result[0].sum_amount, "expect_amount": 600000})
    return render(request, "backend/nav_page/asset_increase.html", {"data_dict": data_dict})


def my_cc(request):
    return None


def cc_marketing(request):
    pass


def cc_list(request):
    pass
