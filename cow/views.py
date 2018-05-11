from django.shortcuts import render, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, logout, authenticate
from cow.dashboard import AssetDashboard
import json
from cow import models
from cow import asset_handle


# Create your views here.

def pages(request, q_all, num):
    '''
    分页功能实现,根据SQL查询内容,设定分多少页,输出
    :param request:
    :param blog_all:
    :return:
    '''
    paginator = Paginator(q_all, num)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    return posts


def index(resquest):
    return render(resquest, 'index.html')


def get_dashboard_data(request):
    dashboard_data = AssetDashboard(request)
    dashboard_data.searilize_page()
    res = json.dumps(dashboard_data.data)
    print(res)

    return HttpResponse(res)


def asset_list(request):
    if request.method == 'GET':
        assets = asset_handle.fetch_asset_list()
        print(assets)
        obj = models.Assets.objects.all()
        data = pages(request, obj, 10)
        print(obj)
        return render(request, 'assets/asset.html', {'assets': assets, 'posts': data})


def asset_detail(request, asset_id):
    if request.method == 'GET':
        try:
            asset_obj = models.Assets.objects.get(id=asset_id)
        except  ObjectDoesNotExist as e:
            print(e)
        return render(request, 'assets/asset_detail.html', {'asset_obj': asset_obj})


def asset_category(request, type):
    assets = asset_handle.fetch_asset_list(type)
    obj = models.Assets.objects.all()
    data = pages(request, obj, 10)
    print(obj)
    return render(request, 'assets/asset.html', {'assets': assets, 'posts': data})
    # return HttpResponse('hahaha')
