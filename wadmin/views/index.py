from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.views import  APIView
from rest_framework.authentication import SessionAuthentication, BaseAuthentication, BasicAuthentication
import time
import hashlib
import json
from wadmin.models import User, LoginStatus
from wadmin.utils.message import Message

# Create your views here.
class Home(APIView):
    def get(self, request):
        return JsonResponse(Message.success(200, None, '后台系统欢迎您！'))

class LoginView(APIView):
    #auth登录页面不需要验证，可设置
    authentication_classes = []  #登录页面不需要认证
    def post(self,request):
        '''
        接收用户名和密码
        :param request:
        :return:
        '''
        param = json.loads(request.body)
        account = param.get('account')
        pwd = param.get('password')
        print(account,pwd)
        obj = User.objects.filter(account=account,password=pwd,enabled=1,status=1).first()
        if not obj:
            return JsonResponse(Message.error(400, '用户名或者密码错误'))
        #创建随机字符串
        ctime = time.time()
        key = '%s|%s'%(account,ctime)
        m = hashlib.md5()
        m.update(key.encode('utf-8'))
        token = m.hexdigest()
        loginObj = LoginStatus.objects.filter(user_id = obj.id).first()
        if not loginObj:
            LoginStatus.objects.create(user_id = obj.id, token = token)
        else:
            loginObj.token = token
            loginObj.status = 1
            loginObj.save()
        return JsonResponse(Message.success(200, token, '登录成功'))

class LogoutView(APIView):
    #auth登录页面不需要验证，可设置
    # authentication_classes = []  #登录页面不需要认证
    def post(self,request):
        '''
        接收用户名和密码
        :param request:
        :return:
        '''
        token = request.META.get("HTTP_TOKEN")
        obj = LoginStatus.objects.filter(token=token, status=1).first()
        if not obj:
            return JsonResponse(Message.error(300, None, '登出失败'))
        obj.status = 0
        obj.save()
        return JsonResponse(Message.success(200, None, '登出成功'))
 
class HostView(APIView):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
 
    # authentication_classes = [MyAuthtication]
 
    def get(self,request,*args,**kwargs):
        print(request.user,'dddddddddddffffff')
        print(request.auth,'dddddddddd')
        #原来的request，django.core.handlers.wsgi.WSGIRequest
        #现在的request ,rest_framework.request.Request
        # print(request)
        # authentication_classes = [SessionAuthentication,BaseAuthentication]
        # print(self.authentication_classes)  # [<class 'rest_framework.authentication.SessionAuthentication'>,
                                            #  <class 'rest_framework.authentication.BasicAuthentication'>]
        # return HttpResponse('GET请求的响应内容')
        return JsonResponse({'code': 200, 'msg': 'GET请求的响应内容', 'obj': None})
 
    def post(self,request,*args,**kwargs):
        pass
        # try:
        #     try :
        #         current_page = request.POST.get("page")
        #
        #         current_page = int(current_page)
        #         int("asd")
        #     except ValueError as e:
        #         print(e)
        #         raise #如果有raise说明自己处理不了了，就交给下面的一个去捕捉了
        # except Exception as e:
        #     print("OK")
        # return  HttpResponse('post请求的响应内容')
        return JsonResponse({'code': 200, 'msg': 'post请求的响应内容', 'obj': None})
 
    def put(self, request, *args, **kwargs):
        # return HttpResponse('put请求的响应内容')
        return JsonResponse({'code': 200, 'msg': 'put请求的响应内容', 'obj': None})