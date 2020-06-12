#coding=utf-8
from django.contrib import admin
from df_user import models
# Register your models here.


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('id','uname', 'upwd', 'uemail', 'ureceive','uaddress','upostcode','uphone',)


admin.site.register(models.UserInfo, UserInfoAdmin)

