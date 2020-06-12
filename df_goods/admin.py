from django.contrib import admin
from df_goods import models
# Register your models here.
class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'ttitle')


class GoodsInfoAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ('id','gtype', 'gtitle', 'gprice', 'gunit','gclick','grest','gbrief','gcontent','isDelete',)


admin.site.register(models.TypeInfo, TypeInfoAdmin)
admin.site.register(models.GoodsInfo, GoodsInfoAdmin)
