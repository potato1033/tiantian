#coding = utf-8
from django.db import models

# Create your models here.
class UserInfo(models.Model):
     uname = models.CharField(max_length=20)
     upwd = models.CharField(max_length=40)
     uemail = models.CharField(max_length=30)
     ureceive = models.CharField(max_length=20, default='',)
     uaddress = models.CharField(max_length=100, default='',)
     upostcode = models.CharField(max_length=6, default='',)
     uphone = models.CharField(max_length=11, default='',)
     #default与blank是python层面的约束，不影响数据库结构，不需要数据库迁移
     def __str__(self):
          # return self.ttitle.encode('utf-8')(python3不能这么写)
          return self.uname

