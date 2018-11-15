from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# from django.core import serializers
from django.forms.models import model_to_dict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.views import  APIView
from rest_framework.authentication import SessionAuthentication, BaseAuthentication, BasicAuthentication
import json
# import logging
from wadmin.models import SQLResource
from wadmin.utils.message import Message
from wadmin.config import PageConfig

class ListView(APIView):
    def post(self,request,*args,**kwargs):
        print('token', request.user)
        print('user', request.auth)
        page = PageConfig['page']
        pageSize = PageConfig['pageSize']
        name = ''
        sql_id = ''
        if request.body:
            param = json.loads(request.body)   
            if param.get('page'):
                page = param.get('page')
            if param.get('pageSize'):
                pageSize = param.get('pageSize')
            if param.get('name'):
                name = param.get('name')
            if param.get('sql_id'):
                sql_id = param.get('sql_id')
        try:
            data = SQLResource.objects.filter(enabled=1, name__contains=name, sql_id__contains=sql_id).values('id','name','seq','status','sql_id','create_time').order_by('seq')
            paginator = Paginator(data, pageSize)
            total = paginator.count
            objs = paginator.page(page)
            # total = SQLResource.objects.filter(enabled=1).count()
            # data = SQLResource.objects.filter(enabled=1).values('id','name','seq','status','sql_id','create_time').order_by('seq')[((page - 1) * pageSize):pageSize]
        except PageNotAnInteger:
            objs = paginator.page(1) 
        except EmptyPage:
            objs = paginator.page(paginator.num_pages)
        except Exception as e:
            print(e)
            return JsonResponse(Message.success(301, None, '获取列表失败！'))
        return JsonResponse(Message.success(200, {'list': list(objs), 'total': total}, '获取列表成功！'))

class AllListView(APIView):
    def post(self,request,*args,**kwargs):
        print('token', request.user)
        print('user', request.auth)
        try:
            data = SQLResource.objects.filter(enabled=1).values('id','name','seq','status','sql_id','create_time').order_by('seq')
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
            data = SQLResource.objects.get(pk=cid, enabled=1)
        except Exception as e:
            print(e)
            return JsonResponse(Message.success(301, None, '获取失败！'))
        return JsonResponse(Message.success(200, model_to_dict(data), '获取成功！'))

class AddView(APIView):
    def post(self,request,*args,**kwargs):
        if not request.body:
            return JsonResponse(Message.success(402, None, '请求入参不正确！'))
        param = json.loads(request.body)
        try:
            SQLResource.objects.create(**param)
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
            obj = SQLResource.objects.get(pk=cid)
            if param.get('name'):
                obj.name = param.get('name')
            if param.get('seq'):
                obj.seq = param.get('seq')
            if param.get('status'):
                obj.status = param.get('status')
            if param.get('sql_id'):
                obj.sql_id = param.get('sql_id')
            if param.get('desc'):
                obj.desc = param.get('desc')
            if param.get('sql_script'):
                obj.desc = param.get('desc')
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
            SQLResource.objects.extra(where=['id IN ('+ idstr +')']).update(enabled=0)
        except:
            return JsonResponse(Message.success(301, None, '删除失败！'))
        return JsonResponse(Message.success(200, None, '删除成功！'))