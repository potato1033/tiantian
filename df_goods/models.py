from django.db import models
from tinymce.models import HTMLField

# Create your models here.
class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)
    def __str__(self):
        #return self.ttitle.encode('utf-8')(python3不能这么写)
        return self.ttitle


class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=20)
    gpic = models.ImageField(upload_to='df_goods')
    gprice = models.DecimalField(max_digits=5,decimal_places=2)#价格最多5位，小数点后占2位
    gunit = models.CharField(max_length=20,default='500g')
    gclick = models.IntegerField()
    gbrief = models.CharField(max_length=200)
    gcontent = HTMLField()
    grest = models.IntegerField()
    gtype = models.ForeignKey(TypeInfo,on_delete='models.CASCADE')
    isDelete = models.BooleanField(default=False)
    #gadvice = models.BooleanField(default=False)
    def __str__(self):
        return self.gtitle