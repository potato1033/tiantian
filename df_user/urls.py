#coding = utf-8
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^register/$', views.register),
    re_path(r'^register_handle/$', views.register_handle),
    re_path(r'^register_exist/$', views.register_exist),
    re_path(r'^login/$', views.login),
    re_path(r'^login_handle/$', views.login_handle),
    re_path(r'^logout/$', views.logout),
    re_path(r'^info/$', views.info),
    re_path(r'^order/(\d+)$', views.order),
    re_path(r'^site/$', views.site),
]