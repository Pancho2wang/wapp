from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# from django.core import serializers
from django.forms.models import model_to_dict
from rest_framework.views import  APIView
from rest_framework.authentication import SessionAuthentication, BaseAuthentication, BasicAuthentication
import json
# import logging
from wadmin.models import Resource
from wadmin.utils.message import Message
from wadmin.config import PageConfig

def dataChangeToTree(data):
    comment_list={}
    for obj in data:
        comment_list[obj['id']]=obj
    ret=[]
    for key in comment_list:
        comment = comment_list[key]
        pid = comment['pid']
        if pid:
            if comment_list[pid].get('chilren') is None:
                comment_list[pid].setdefault('children', [])
            comment_list[pid]['children'].append(comment)
        else:
            ret.append(comment)
    return ret

class ListView(APIView):
    def post(self,request,*args,**kwargs):
        print('token', request.user)
        print('user', request.auth)
        try:
            data = Resource.objects.filter(enabled=1).values('id','pid','name','seq','status','per_type','url','icon','create_time').order_by('seq')
            data = dataChangeToTree(list(data))
        except Exception as e:
            print(e)
            return JsonResponse(Message.success(301, None, '获取列表失败！'))
        return JsonResponse(Message.success(200, {'list': data}, '获取列表成功！'))

class PListView(APIView):
    def post(self,request,*args,**kwargs):
        print('token', request.user)
        print('user', request.auth)
        try:
            data = Resource.objects.filter(enabled=1).values('id','name', 'pid').order_by('seq')
            data = dataChangeToTree(list(data))
        except Exception as e:
            print(e)
            return JsonResponse(Message.success(301, None, '获取列表失败！'))
        return JsonResponse(Message.success(200, {'list': data}, '获取列表成功！'))

class OneByIdView(APIView):
    def post(self,request,*args,**kwargs):
        if not request.body:
            return JsonResponse(Message.success(402, None, '请求入参不正确！'))
        param = json.loads(request.body)
        cid = param.get('id')
        if not cid:
            return JsonResponse(Message.success(402, None, '请求入参不正确！'))
        try:
            data = Resource.objects.filter(pk=cid,enabled=1).values('id','pid','name','seq','status','per_type','url','icon','desc').first()
        except Exception as e:
            print(e)
            return JsonResponse(Message.success(301, None, '获取失败！'))
        # return JsonResponse(Message.success(200, model_to_dict(data), '获取成功！'))
        return JsonResponse(Message.success(200, data, '获取成功！'))

class AddView(APIView):
    def post(self,request,*args,**kwargs):
        if not request.body:
            return JsonResponse(Message.success(402, None, '请求入参不正确！'))
        param = json.loads(request.body)
        try:
            obj = Resource()
            if param.get('name'):
                obj.name = param.get('name')
            if param.get('seq'):
                obj.seq = param.get('seq')
            if param.get('status'):
                obj.status = param.get('status')
            if param.get('pid'):
                obj.pid = Resource.objects.get(pk=param.get('pid'))
            if param.get('per_type'):
                obj.per_type = param.get('per_type')
            if param.get('url'):
                obj.url = param.get('url')
            if param.get('icon'):
                obj.icon = param.get('icon')
            if param.get('desc'):
                obj.desc = param.get('desc')
            obj.save()
        except Exception as e:
            print(e)
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
            obj = Resource.objects.get(pk=cid)
            if param.get('name'):
                obj.name = param.get('name')
            if param.get('seq'):
                obj.seq = param.get('seq')
            if param.get('status'):
                obj.status = param.get('status')
            if param.get('pid'):
                obj.pid = Resource.objects.get(pk=param.get('pid'))
            if param.get('per_type'):
                obj.per_type = param.get('per_type')
            if param.get('url'):
                obj.url = param.get('url')
            if param.get('icon'):
                obj.icon = param.get('icon')
            if param.get('desc'):
                obj.desc = param.get('desc')
            obj.save()
        except Exception as e:
            print(e)
            return JsonResponse(Message.success(301, None, '更新失败！'))
        return JsonResponse(Message.success(200, None, '更新成功！'))

class DeleteView(APIView):
    def post(self, request, *args, **kwargs):
        if not request.body:
            return JsonResponse(Message.success(402, None, '请求入参不正确！'))
        param = json.loads(request.body)
        cid = param.get('id')
        if not cid:
            return JsonResponse(Message.success(402, None, '请求入参不正确！'))
        try:
            obj = Resource.objects.get(pk=cid)
            obj.enabled = 0
            obj.save()
        except Exception as e:
            print(e)
            return JsonResponse(Message.success(301, None, '删除失败！'))
        return JsonResponse(Message.success(200, None, '删除成功！'))