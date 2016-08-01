from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest.models import Platform, User
from rest.serialzers import PlatformSerializer, UserSerializer


#TODO:使用access_token限制用户访问

@api_view(['GET', 'POST'])
def login(request, format=None):
    if request.method == "GET":
        user_name = request.GET.get("user_name")
        password = request.GET.get("password")
        try:
            user = User.objects.get(user_name=user_name)
            assert user.password == password , "用户名密码不正确"
            assert user.status == "S", "用户状态不正常"
        except User.DoesNotExist:
            return Response({"code":"F","msg":"无此用户"})
        except AssertionError as e:
            return Response({"code":"F", "msg":e})
        user_serial = UserSerializer(user)
        return Response(user_serial.data)
    else:
        pass


@api_view(['GET','POST'])
def register(request, format=None):
    if request.method == "GET":
        user_name = request.GET.get("user_name")
        password = request.GET.get("password")
        try:
            assert user_name is not None and len(user_name) > 3 , "用户名格式不正确"
            assert password is not None and len(password) > 3, "密码格式不正确"
            user = User(user_name = user_name, password=password)
            user.save()
        except AssertionError as e:
            return Response({"code":"F", "msg":e})
        return Response({"code":"S", "msg":"注册成功"})
    else:
        pass

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
