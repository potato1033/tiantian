#coding=utf-8
import django.http
from django.shortcuts import render
from df_user.models import *
from df_cart.models import *
from .models import *
from df_user import user_decorator
from django.http import JsonResponse, HttpResponse
from django.db import transaction
from decimal import Decimal
from datetime import datetime
# Create your views here.
import df_user.models


@user_decorator.login
def order(request):
    uid = request.session['user_id']
    user = UserInfo.objects.get(id=uid)
    cart_ids = request.GET.getlist('cart_id')
    carts = []
    total0 = {}
    total_price = 0
    ccount = len(cart_ids)
    for cid in cart_ids:
        cart = CartInfo.objects.get(id=cid)
        carts.append(cart)
        tprice = int(cart.count) * float(cart.goods.gprice)
        total_price += tprice#除去运费总价

    total_price = float('%0.2f' % total_price)
    trans_cost = 10
    total_trans_price = total_price + trans_cost #总价加上运费

    con = {
        'title': '提交订单', 'page_name': 1,
        'user': user, 'carts': carts,
        'total_price': float('%0.2f' % total_price),
        'trans_cost': trans_cost,
        'total_trans_price': total_trans_price,
        'ccount': ccount,
        }
    return render(request, 'df_order/order.html', con)



@user_decorator.login
@transaction.atomic()  # 事务
def order_handle(request):
    tran_id = transaction.savepoint()  # 保存事务发生点
    cart_ids = request.POST.get('cart_ids')  # 用户提交的订单购物车，此时cart_ids为字符串，例如'1,2,3,'
    user_id = request.session['user_id']  # 获取当前用户的id
    user = UserInfo.objects.get(id=user_id)
    data = {}
    try:
        order_info = OrderInfo()  # 创建一个订单对象
        now = datetime.now()
        order_info.oid = '%s%d' % (now.strftime('%Y%m%d%H%M%S'), user_id)  # 订单号为订单提交时间和用户id的拼接
        order_info.odate = now  # 订单时间
        order_info.user_id = int(user_id)  # 订单的用户id
        order_info.ototal = Decimal(request.POST.get('total'))  # 从前端获取的订单总价
        order_info.oreceive = user.ureceive
        order_info.oaddress = user.uaddress
        order_info.opostcode = user.upostcode
        order_info.ophone = user.uphone
        order_info.save()  # 保存订单
        cart_idsl = cart_ids.split(',')
        for cart_id in cart_idsl:  # 逐个对用户提交订单中的每类商品即每一个小购物车
            cart = CartInfo.objects.get(pk=cart_id)  # 从CartInfo表中获取小购物车对象
            order_detail = OrderDetailInfo()  # 大订单中的每一个小商品订单
            order_detail.order = order_info  # 外键关联，小订单与大订单绑定
            goods = cart.goods  # 具体商品
            if cart.count <= goods.grest:  # 判断库存是否满足订单，如果满足，修改数据库
                goods.grest = goods.grest - cart.count
                goods.save()
                order_detail.goods = goods
                order_detail.price = goods.gprice
                order_detail.count = cart.count
                order_detail.save()
                cart.delete()  # 并删除当前购物车
            else:  # 否则，则事务回滚，订单取消
                transaction.savepoint_rollback(tran_id)
                data = {}
                data['ok'] = 2
                return JsonResponse(data)
                #return HttpResponse('库存不足')
        data['ok'] = 1
        transaction.savepoint_commit(tran_id)
    except Exception as e:
        print("%s" % e)
        print('未完成订单提交')
        transaction.savepoint_rollback(tran_id)  # 事务任何一个环节出错，则事务全部取消
    return JsonResponse(data)


@user_decorator.login
def pay(request):
    pass
