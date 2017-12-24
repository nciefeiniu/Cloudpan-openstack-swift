# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from keystoneclient.v3 import client as keystoneclient
from keystoneauth1.identity import v3
from keystoneauth1 import session
from swiftclient import client
from django.http import StreamingHttpResponse
import os

#连接
def conns(username, password):

    # 认证
    _authurl = 'http://127.0.0.1:5000/v3/'
    _auth_version = '3'
    _user = username
    _key = password
    _os_options = {
        'user_domain_name': 'default',
        'project_domain_name': 'default',
        'project_name': 'demo'
    }

    conn = client.Connection(
        authurl=_authurl,
        user=_user,
        key=_key,
        os_options=_os_options,
        auth_version=_auth_version
    )
    return conn

# Create your views here.
def index(request):
    username = request.session['username']
    password = request.session['password']
    conn = conns(username, password)
    #列出可用的容器
    resp_headers, containers = conn.get_account()
    print(containers)
    #显示哪一个
    if request.GET['dir'] != '':
       container = request.GET['dir']
    else:
        container = containers[0]['name']
    print("Response headers: %s" % resp_headers)
    for container2 in containers:
        print(container2)

    test = conn.get_container(container)
    return render(request, 'lpan/index.html', { 'con_name':container,'containers':containers,'test':containers[0]['name'], 'test2':test[1], 'test3':test[1]})

#下载
def download(request):
    username = request.session['username']
    password = request.session['password']
    conn = conns(username, password)
    obj = request.GET['filename']
    # obj = 'test.txt'
    container = request.GET['con_name']
    containers = conn.get_account()
    resp_headers, obj_contents = conn.get_object(container, obj)
    response = StreamingHttpResponse(obj_contents)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(obj)
    return response

#上传
def upload(request):
    username = request.session['username']
    password = request.session['password']
    conn = conns(username, password)
    container = request.GET['con_name']
    # container = 'new-container'
    if request.method == "POST":    # 请求方法为POST时，进行处理
        myFile =request.FILES.get("exampleInputFile")    # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            return HttpResponse("no files for upload!")
        # destination = open(os.path.join("E:\\upload",myFile.name),'wb+')    # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():      # 分块写入文件
            # destination.write(chunk)
            conn.put_object(
                container,
                myFile.name,
                contents='local',
                content_type='text/plain'
            )
        # destination.close()
            return HttpResponseRedirect('/lpan/?dir='+container)
    else:
        return HttpResponseRedirect('/lpan/?dir='+container)

#删除对象
def delete(request):
    obj = request.GET['file_name']
    username = request.session['username']
    password = request.session['password']
    conn = conns(username, password)
    container = request.GET['con_name']
    try:
        conn.delete_object(container, obj)
        print("Successfully deleted the object")
    except:
        print("Failed to delete the object with error: %s" )
    else:
        return HttpResponseRedirect('/lpan/?dir=new-container#')

#登录
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        _authurl = 'http://127.0.0.1:5000/v3/'
        _auth_version = '3'
        _user = 'demo'
        _key = '0901'
        _os_options = {
            'user_domain_name': 'default',
            'project_domain_name': 'default',
            'project_name': 'demo'
        }
        try:
            conn = client.Connection(
                authurl=_authurl,
                user=username,
                key=password,
                os_options=_os_options,
                auth_version=_auth_version
            )
            resp_headers, containers = conn.get_account()
        except client.ClientException:
            return HttpResponseRedirect("/lpan/login/")
        else:
            request.session['username'] = username
            request.session['password'] = password
            return HttpResponseRedirect('/lpan/?dir=')
    else:
        return render(request, 'lpan/login.html')

#注册
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        print(username)
        if password != password2:
            return HttpResponseRedirect('/lpan/register')
        try:
            test = v3.user.UserManager.create(
                username,domain='default',project='demo',password='password'
            )
            print(test)
        except:
            pass
        else:
            return HttpResponse("OK")
    else:
        return render(request, 'lpan/register.html')

#创建一个新的容器
def create_container(request):
    if request.method == 'POST':
        container_name = request.POST['con_name']
        username = request.session['username']
        password = request.session['password']
        conn = conns(username, password)
        container = container_name
        conn.put_container(container)
        resp_headers, containers = conn.get_account()
        return HttpResponseRedirect('/lpan/?dir=new-container#')
    else:
        return render(requet, 'lpan/add.html')

#删除容器
def delete_container(request):
    container_name = request.GET['con_name']
    username = request.session['username']
    password = request.session['password']
    conn = conns(username, password)
    try:
        conn.delete_container(container_name)
    except:
        return HttpResponseRedirect('/lpan/?dir=new-container#')
    else:
        return HttpResponseRedirect('/lpan/?dir=new-container#')
