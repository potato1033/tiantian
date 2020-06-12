#coding = utf-8
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.order),
    re_path(r'^push/$', views.order_handle),
    re_path(r'^pay/$', views.pay)
]