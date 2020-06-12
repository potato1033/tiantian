#coding=utf-8
from django.http import HttpResponseRedirect

#如果未登录成功则返回登录页面
def login(func):#func为装饰器装饰的函数
    def login_fun(request, *args, **kwargs):
        if request.session.has_key('user_id'):
            return func(request, *args, **kwargs) #加*args, ** kwargs是因为被装饰的函数参数数目不一定
        else:
            red = HttpResponseRedirect('/user/login/')
            red.set_cookie('url', request.get_full_path())#要求登录后返回原来页面
            return red
    return login_fun

'''
http://127.0.0.1:8000/200/?type=10
request.path: 表示当前路径，为/200
request.get_full_path: 表示完整路径，为/200/?type=10
'''
