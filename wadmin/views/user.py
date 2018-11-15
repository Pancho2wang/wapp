from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# from django.core import serializers
from django.forms.models import model_to_dict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.views import  APIView
from rest_framework.authentication import SessionAuthentication, BaseAuthentication, BasicAuthentication
import json
# import logging
from wadmin.models import User,Role,Company
from wadmin.utils.message import Message
from wadmin.config import PageConfig

class ListView(APIView):
    def post(self,request,*args,**kwargs):
        print('token', request.user)
        print('user', request.auth)
        page = PageConfig['page']
        pageSize = PageConfig['pageSize']
        name = ''
        account = ''
        if request.body:
            param = json.loads(request.body)   
            if param.get('page'):
                page = param.get('page')
            if param.get('pageSize'):
                pageSize = param.get('pageSize')
            if param.get('account'):
                account = param.get('account')
            if param.get('name'):
                name = param.get('name')
        try:
            data = User.objects.filter(enabled=1,account__contains=account,name__contains=name).values('id','account','status','name','user_type','create_time').order_by('id')
            paginator = Paginator(data, pageSize)
            total = paginator.count
            users = paginator.page(page)
            # total = User.objects.filter(enabled=1).count()
            # data = User.objects.filter(enabled=1).values('id','account','status','name','user_type','create_time')[((page - 1) * pageSize):pageSize]
        except PageNotAnInteger:
            users = paginator.page(1) 
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        except Exception as e:
            print(e)
            return JsonResponse(Message.success(301, None, '获取列表失败！'))
        return JsonResponse(Message.success(200, {'list': list(users), 'total': total}, '获取列表成功！'))

class OneByIdView(APIView):
    def post(self,request,*args,**kwargs):
        if not request.body:
            return JsonResponse(Message.success(402, None, '请求入参不正确！'))
        param = json.loads(request.body)
        cid = param.get('id')
        if not cid:
            return JsonResponse(Message.success(402, None, '请求入参不正确！'))
        try:
            obj = User.objects.get(pk=cid,enabled=1)
            roleList = obj.roles.filter(enabled=1).values('id')
            roles = []
            for role in roleList:
                roles.append(role['id'])
            companyList = obj.companys.filter(enabled=1).values('id')
            companys = []
            for company in companyList:
                companys.append(company['id'])
            data = model_to_dict(obj)
            data['roles'] = roles
            data['companys'] = companys
        except Exception as e:
            print(e)
            return JsonResponse(Message.success(301, None, '获取失败！'))
        return JsonResponse(Message.success(200, data, '获取成功！'))

class AddView(APIView):
    def post(self,request,*args,**kwargs):
        if not request.body:
            return JsonResponse(Message.success(402, None, '请求入参不正确！'))
        param = json.loads(request.body)
        try:
            obj = User()
            if param.get('account'):
                obj.account = param.get('account')
            if param.get('password'):
                obj.password = param.get('password')
            if param.get('name'):
                obj.name = param.get('name')
            if param.get('status'):
                obj.status = param.get('status')
            if param.get('user_type'):
                obj.user_type = param.get('user_type')
            obj.save()
            if param.get('companys'):
                cIds = ','.join(str(s) for s in param.get('companys'))
                obj.companys.set(Company.objects.extra(where=['id IN ('+ cIds +')']))
            else:
                obj.companys.clear()
            if param.get('roles'):
                rIds = ','.join(str(s) for s in param.get('roles'))
                obj.roles.set(Role.objects.extra(where=['id IN ('+ rIds +')']))
            else:
                obj.roles.clear()
            obj.save()
        except:
            return JsonResponse(Message.success(301, None, '新增失败！'))
        return JsonResponse(Message.success(200, None, '新增成功！'))

class UpdateView(APIView):
    def post(self,request,*args,**kwargs):
        if not request.body:
            return JsonResponse(Message.success(402, None, '请求入参不正确！'))
        param = json.loads(request.body)
        cid = param.get('id')
        if not cid:
            return JsonResponse(Message.success(402, None, '请求入参不正确！'))
        try:
            obj = User.objects.get(pk=cid)
            if param.get('password'):
                obj.password = param.get('password')
            if param.get('name'):
                obj.name = param.get('name')
            if param.get('status'):
                obj.status = param.get('status')
            if param.get('user_type'):
                obj.user_type = param.get('user_type')
            obj.save()
            if param.get('companys'):
                cIds = ','.join(str(s) for s in param.get('companys'))
                obj.companys.set(Company.objects.extra(where=['id IN ('+ cIds +')']))
            else:
                obj.companys.clear()
            if param.get('roles'):
                rIds = ','.join(str(s) for s in param.get('roles'))
                obj.roles.set(Role.objects.extra(where=['id IN ('+ rIds +')']))
            else:
                obj.roles.clear()
            obj.save()
        except:
            return JsonResponse(Message.success(301, None, '更新失败！'))
        return JsonResponse(Message.success(200, None, '更新成功！'))

class DeleteView(APIView):
    def post(self, request, *args, **kwargs):
        if not request.body:
            return JsonResponse(Message.success(402, None, '请求入参不正确！'))
        param = json.loads(request.body)
        ids = param.get('ids')
        if not ids:
            return JsonResponse(Message.success(402, None, '请求入参不正确！'))
        try:
            idstr = ','.join(str(s) for s in ids)
            User.objects.extra(where=['id IN ('+ idstr +')']).update(enabled=0)
        except Exception as e:
            print(e)
            return JsonResponse(Message.success(301, None, '删除失败！'))
        return JsonResponse(Message.success(200, None, '删除成功！'))