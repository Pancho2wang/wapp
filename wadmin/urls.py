from django.urls import path

from wadmin.views.index import *
import wadmin.views.company as Company
import wadmin.views.role as Role
import wadmin.views.user as User
import wadmin.views.resource as Resource
import wadmin.views.sqlresource as SQLResource

urlpatterns = [
    path('', Home.as_view(), name='index'),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),

    path('company/list', Company.ListView.as_view()),
    path('company/allList', Company.AllListView.as_view()),
    path('company/getOneById', Company.OneByIdView.as_view()),
    path('company/add', Company.AddView.as_view()),
    path('company/update', Company.UpdateView.as_view()),
    path('company/delete', Company.DeleteView.as_view()),

    path('role/list', Role.ListView.as_view()),
    path('role/allList', Role.AllListView.as_view()),
    path('role/getOneById', Role.OneByIdView.as_view()),
    path('role/add', Role.AddView.as_view()),
    path('role/update', Role.UpdateView.as_view()),
    path('role/delete', Role.DeleteView.as_view()),

    path('user/list', User.ListView.as_view()),
    path('user/getOneById', User.OneByIdView.as_view()),
    path('user/add', User.AddView.as_view()),
    path('user/update', User.UpdateView.as_view()),
    path('user/delete', User.DeleteView.as_view()),

    path('resource/list', Resource.ListView.as_view()),
    path('resource/plist', Resource.PListView.as_view()),
    path('resource/getOneById', Resource.OneByIdView.as_view()),
    path('resource/add', Resource.AddView.as_view()),
    path('resource/update', Resource.UpdateView.as_view()),
    path('resource/delete', Resource.DeleteView.as_view()),

    path('sqlresource/list', SQLResource.ListView.as_view()),
    path('sqlresource/allList', SQLResource.AllListView.as_view()),
    path('sqlresource/getOneById', SQLResource.OneByIdView.as_view()),
    path('sqlresource/add', SQLResource.AddView.as_view()),
    path('sqlresource/update', SQLResource.UpdateView.as_view()),
    path('sqlresource/delete', SQLResource.DeleteView.as_view()),

    path('hosts', HostView.as_view()),
]