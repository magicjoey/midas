from django.db import IntegrityError
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
    return None