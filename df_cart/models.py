from django.db import models

#谁买了几个什么商品
class CartInfo(models.Model):
    user = models.ForeignKey('df_user.UserInfo',on_delete='models.CASCADE')
    goods = models.ForeignKey('df_goods.GoodsInfo',on_delete='models.CASCADE')
    count = models.IntegerField()
    total = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

'''
由于用户与商品存在多对多的关系，即一个用户可以对应多个商品，一个商品也可以对应多个用户
所以引入购物车表CartInfo来维护信息
购物车与用户、商品均为一对多的关系，即购物车表的一条信息只对应一个用户，一个商品
再引入数量来记录商品数目
'''