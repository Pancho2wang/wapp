from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# from django.core import serializers
from django.forms.models import model_to_dict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.views import  APIView
from rest_framework.authentication import SessionAuthentication, BaseAuthentication, BasicAuthentication
import json
# import logging
from wadmin.models import Role,Resource,SQLResource
from wadmin.utils.message import Message
from wadmin.config import PageConfig

class ListView(APIView):
    def post(self,request,*args,**kwargs):
        print('token', request.user)
        print('user', request.auth)
        page = PageConfig['page']
        pageSize = PageConfig['pageSize']
        name = ''
        if request.body:
            param = json.loads(request.body)   
            if param.get('page'):
                page = param.get('page')
            if param.get('pageSize'):
                pageSize = param.get('pageSize')
            if param.get('name'):
                name = param.get('name')
        try:
            data = Role.objects.filter(enabled=1, name__contains=name).values('id','name','seq','status','alias_name','is_all_sql_auth','create_time').order_by('seq')
            paginator = Paginator(data, pageSize)
            total = paginator.count
            roles = paginator.page(page)
            # total = Role.objects.filter(enabled=1).count()
            # data = Role.objects.filter(enabled=1).values('id','name','seq','status','alias_name','is_all_sql_auth','create_time').order_by('seq')[((page - 1) * pageSize):pageSize]
        except PageNotAnInteger:
            roles = paginator.page(1) 
        except EmptyPage:
            roles = paginator.page(paginator.num_pages)
        except Exception as e:
            print(e)
            return JsonResponse(Message.success(301, None, '获取列表失败！'))
        return JsonResponse(Message.success(200, {'list': list(roles), 'total': total}, '获取列表成功！'))

class AllListView(APIView):
    def post(self,request,*args,**kwargs):
        print('token', request.user)
        print('user', request.auth)
        try:
            data = Role.objects.filter(enabled=1).values('id','name','seq','status','alias_name').order_by('seq')
        except Exception as e:
            print(e)
            return JsonResponse(Message.success(301, None, '获取列表失败！'))
        return JsonResponse(Message.success(200, {'list': list(data)}, '获取列表成功！'))

class OneByIdView(APIView):
    def post(self,request,*args,**kwargs):
        if not request.body:
            return JsonResponse(Message.success(402, None, '请求入参不正确！'))
        param = json.loads(request.body)
        cid = param.get('id')
        if not cid:
            return JsonResponse(Message.success(402, None, '请求入参不正确！'))
        try:
            # data = Role.objects.get(pk=cid)
            obj = Role.objects.get(pk=cid,enabled=1)
            resourceList = obj.resources.filter(enabled=1).values('id')
            resources = []
            for resource in resourceList:
                resources.append(resource['id'])
            sqlResourceList = obj.sql_resources.filter(enabled=1).values('id')
            sqlResources = []
            for sqlResource in sqlResourceList:
                sqlResources.append(sqlResource['id'])
            data = model_to_dict(obj)
            data['resources'] = resources
            data['sql_resources'] = sqlResources
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
            # Role.objects.create(**param)
            obj = Role()
            if param.get('name'):
                obj.name = param.get('name')
            if param.get('seq'):
                obj.seq = param.get('seq')
            if param.get('alias_name'):
                obj.alias_name = param.get('alias_name')
            if param.get('status'):
                obj.status = param.get('status')
            if param.get('is_all_sql_auth'):
                obj.is_all_sql_auth = param.get('is_all_sql_auth')
            if param.get('desc'):
                obj.desc = param.get('desc')
            obj.save()
            if param.get('resources'):
                rIds = ','.join(str(s) for s in param.get('resources'))
                obj.resources.set(Resource.objects.extra(where=['id IN ('+ rIds +')']))
            else:
                obj.resources.clear()
            if param.get('sql_resources'):
                sIds = ','.join(str(s) for s in param.get('sql_resources'))
                obj.sql_resources.set(SQLResource.objects.extra(where=['id IN ('+ sIds +')']))
            else:
                obj.sql_resources.clear()
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
            obj = Role.objects.get(pk=cid)
            if param.get('name'):
                obj.name = param.get('name')
            if param.get('seq'):
                obj.seq = param.get('seq')
            if param.get('status'):
                obj.status = param.get('status')
            if param.get('alias_name'):
                obj.alias_name = param.get('alias_name')
            if param.get('is_all_sql_auth'):
                obj.is_all_sql_auth = param.get('is_all_sql_auth')
            if param.get('desc'):
                obj.desc = param.get('desc')
            obj.save()
            if param.get('resources'):
                rIds = ','.join(str(s) for s in param.get('resources'))
                obj.resources.set(Resource.objects.extra(where=['id IN ('+ rIds +')']))
            else:
                obj.resources.clear()
            if param.get('sql_resources'):
                sIds = ','.join(str(s) for s in param.get('sql_resources'))
                obj.sql_resources.set(SQLResource.objects.extra(where=['id IN ('+ sIds +')']))
            else:
                obj.sql_resources.clear()
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
            Role.objects.extra(where=['id IN ('+ idstr +')']).update(enabled=0)
        except Exception as e:
            print(e)
            return JsonResponse(Message.success(301, None, '删除失败！'))
        return JsonResponse(Message.success(200, None, '删除成功！'))