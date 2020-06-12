#coding = utf-8
import django.core.paginator
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

import df_order.models
from .models import *
from hashlib import sha1
from . import user_decorator
from df_goods.models import GoodsInfo
from df_order.models import OrderInfo
from django.core.paginator import Paginator
# Create your views here.


def register(request):
    con = {'title': '用户注册',}
    return render(request, 'df_user/register.html', con)


def register_handle(request):
    #接收用户输入
    post = request.POST
    uname =post.get("user_name")
    upwd = post.get("pwd")
    upwd2 = post.get("cpwd")
    uemail = post.get("email")
    #判断两次密码
    if upwd != upwd2:
        return redirect('/user/register/')
    #密码加密
    s1 = sha1()
    s1.update(upwd.encode("utf8"))
    upw3 = s1.hexdigest()
    #创建实例
    user = UserInfo()
    user.uname = uname
    user.upwd = upw3
    user.uemail = uemail
    user.save()
    #注册成功转到登陆页面
    return redirect('/user/login/')


def register_exist(request):
    get = request.GET
    uname = get.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count': count})


def login(request):
    uname = request.COOKIES.get('uname', '')
    con = {'title': '用户登录', 'error_name': 0, 'error_pwd': 0, 'uname': uname, }
    return render(request, 'df_user/login.html', context=con)


def login_handle(request):
    #接受请求
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    remember = post.get("remember", 0)
    #根据用户名查找对象
    users = UserInfo.objects.filter(uname=uname) #使用filter方法，uname不存在返回[]
    #判断：如果未查到则用户名错，如果查到则判断密码是否错误，正确则返回用户中心
    if len(users) == 1:
        s1 = sha1()
        s1.update(upwd.encode("utf8"))
        if s1.hexdigest() == users[0].upwd:
            rtd = HttpResponseRedirect('/user/info/')
            if remember != 0:
                rtd.set_cookie('uname', uname)
            else:
                rtd.set_cookie('uname', '', max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            return rtd
        else:
            con = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname, 'upwd': upwd, }
            return render(request, 'df_user/login.html', context=con)
    else:
        con = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname, 'upwd': upwd, }
        return render(request, 'df_user/login.html',context=con )


def logout(request):
    data = {}
    try:
        request.session.flush()
        data = {'ok':1}
    except Exception as e:
        pass
    #return redirect('/')
    return JsonResponse(data)


@user_decorator.login
def info(request):
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail
    user_address = UserInfo.objects.get(id=request.session['user_id']).uaddress
    #从cookies中读取goods_ids，并查询数据库中对应的goods
    goods_ids = request.COOKIES.get('goods_ids','')
    goods_idl = goods_ids.split(',')
    #GoodsInfo.objects.filter(id__in == goods_idl) #查询出来的是按id排序的
    goods_list = []
    if goods_ids != '':
        for goods_id in goods_idl:
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))

    con = {'title': '用户中心', 'user_email': user_email,
           'user_name': request.session['user_name'],
           'user_address': user_address,
           'page_name': 1,
           'goods_list': goods_list, }
    return render(request, 'df_user/user_center_info.html',con)


@user_decorator.login
def order(request,index):
    user_id = request.session['user_id']
    orders_list = OrderInfo.objects.filter(user_id=int(user_id)).order_by('-odate')
    paginator = Paginator(orders_list, 2)
    page = paginator.page(int(index))
    con = {'title': '用户中心', 'page_name': 1,
           'paginator': paginator,
           'page': page,}
    return render(request, 'df_user/user_center_order.html',con)


@user_decorator.login
def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method=='POST':
        post = request.POST
        user.ureceive = post.get('ureceive')
        user.uaddress = post.get('uaddress')
        user.upostcode = post.get('upostcode')
        user.uphone = post.get('uphone')
        user.save()
    con = {'title': '用户中心','user': user, 'page_name': 1,}
    return render(request, 'df_user/user_center_site.html',con)