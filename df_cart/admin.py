#coding=utf-8
from django.contrib import admin
from df_cart import models
# Register your models here.


class CartInfoAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ('user','goods', 'count', )


admin.site.register(models.CartInfo, CartInfoAdmin)
