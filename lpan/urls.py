# _*_ coding:utf-8 _*_
#Author: liutao

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^download/$', views.download, name='download'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^delete/$', views.delete, name='delete'),
    url(r'^create_container/$', views.create_container, name='create_container'),
    url(r'^delete_container/$', views.delete_container, name='delete_container'),
]
