from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view

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
    if check_login(request):
        login_user = get_login_user(request)
        return render(request, "backend/nav_page/dashboard.html", {})
    else:
        return HttpResponseRedirect("/login?code=S&msg=请登录")


def account(request):
    if check_login(request):
        login_user = get_login_user(request)
        return render(request, "backend/nav_page/account.html", {})
    else:
        return HttpResponseRedirect("/login?code=S&msg=请登录")


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