#coding=utf-8
from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator, Page
from df_cart.models import CartInfo
from haystack.views import SearchView
# Create your views here.


def index(request):
    ccount = cart_count(request)
    #查询每个类型的最新的4条、最热的4条数据
    typelist = TypeInfo.objects.all()
    type0 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    type01 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]
    type1 = typelist[1].goodsinfo_set.order_by('-id')[0:4]
    type11 = typelist[1].goodsinfo_set.order_by('-gclick')[0:4]
    type2 = typelist[2].goodsinfo_set.order_by('-id')[0:4]
    type21 = typelist[2].goodsinfo_set.order_by('-gclick')[0:4]
    type3 = typelist[3].goodsinfo_set.order_by('-id')[0:4]
    type31 = typelist[3].goodsinfo_set.order_by('-gclick')[0:4]
    type4 = typelist[4].goodsinfo_set.order_by('-id')[0:4]
    type41 = typelist[4].goodsinfo_set.order_by('-gclick')[0:4]
    type5 = typelist[5].goodsinfo_set.order_by('-id')[0:4]
    type51 = typelist[5].goodsinfo_set.order_by('-gclick')[0:4]
    con = {'title': '首页', 'guest_cart': 1, 'ccount': ccount,
           'type0': type0, 'type01': type01,
           'type1': type1, 'type11': type11,
           'type2': type2, 'type21': type21,
           'type3': type3, 'type31': type31,
           'type4': type4, 'type41': type41,
           'type5': type5, 'type51': type51,}
    return render(request, 'df_goods/index.html', con ,)


def list(request, tid, pindex, sort):
    ccount = cart_count(request)
    typeinfo = TypeInfo.objects.get(pk=int(tid))
    news = typeinfo.goodsinfo_set.order_by('-id')[0:2]
    if sort == '1':#默认，按最新的排序
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-id')
    elif sort == '2':#按价格排序
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gprice')
    elif sort == '3':#按人气（点击量）排序
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gclick')
    paginator = Paginator(goods_list, 10) #分页，每页最多10个商品
    page = paginator.page(int(pindex))
    con = {'title': typeinfo.ttitle, 'guest_cart': 1,
           'page': page,
           'paginator': paginator,
           'typeinfo': typeinfo,
           'sort': sort,
           'news': news,
           'ccount': ccount, }
    return render(request, 'df_goods/list.html', con)


def detail(request, id):
    ccount = cart_count(request)
    goods = GoodsInfo.objects.get(pk=int(id))
    goods.gclick += 1#点击过，点击量+1
    goods.save()
    typeinfo = TypeInfo.objects.get(ttitle=goods.gtype)
    news = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    con = {'title': goods.gtype.ttitle, 'guest_cart': 1,
           'typeinfo': typeinfo,
           'g': goods,
           'id': id,
           'news': news,
           'ccount': ccount,}
    red = render(request, 'df_goods/detail.html', con)

    #使用cookie记录最近浏览，在用户中心使用
    goods_ids = request.COOKIES.get('goods_ids','')#cookies中没有'goods_ids'键，则另goods_ids: ''
    goods_id = '%d'%goods.id
    if goods_ids != '':##如果cookies中有'goods_ids'
        goods_idsl = goods_ids.split(',')#将长字符串切割为字符串列表
        if goods_idsl.count(goods_id) >= 1:#判断列表中是否存在该商品id
            goods_idsl.remove(goods_id)    #有则删除该商品id
        goods_idsl.insert(0,goods_id)      #然后将该商品id加到列表最前边
        if len(goods_idsl)>=6:    #如果列表中元素超过5个
            del goods_idsl[5]    #删除最后一个
        goods_ids = ','.join(goods_idsl)#将字符串列表拼接为长字符串
    else:  #如果cookies中没有'goods_ids'，直接将goods_id写入goods_ids
        goods_ids = goods_id
    red.set_cookie('goods_ids',goods_ids)#写入cookies
    return red


def cart_count(request):
    if 'user_id'in request.session:
        return CartInfo.objects.filter(user_id=request.session['user_id']).count()
    else:
        return 0

#继承haystack.views中的SearchView类，自定义函数为模板返回参数
class MySearchView(SearchView):
    def extra_context(self):
        con = super(MySearchView, self).extra_context()
        con['title'] = '搜索'
        con['guest_cart'] = 1
        con['ccount'] = cart_count(self.request)
        return con
