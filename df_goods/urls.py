#coding = utf-8
from django.urls import re_path
from . import views
from .views import * #把views.py中的类引用过来

urlpatterns = [
    re_path(r'^$', views.index),
    re_path(r'^list(\d+)_(\d+)_(\d+)/$', views.list),
    re_path(r'^(\d+)/$', views.detail),
    re_path(r'^search/$',MySearchView())
]