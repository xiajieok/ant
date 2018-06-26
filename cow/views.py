from django.shortcuts import render, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from cow.serializers import UserSerializer, GroupSerializer

from django.contrib.auth import login, logout, authenticate
from cow.dashboard import AssetDashboard
import json
from django.http import JsonResponse
from cow import models
from cow import asset_handle
import os

import datetime

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        # if isinstance(obj, datetime):
        # return obj.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(obj, datetime.date):
            return obj.strftime('%H:%M')
        else:
            return json.JSONEncoder.default(self, obj)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
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
        obj = models.Assets.objects.all()
        data = pages(request, obj, 10)
        print('new', obj)
        return render(request, 'assets/asset.html', {'assets': assets, 'posts': data})


def asset_detail(request,asset_id):
    print(request.GET.get('type'))
    if request.method == 'GET':
        if request.GET.get('type') is None:
            try:
                asset_obj = models.Assets.objects.get(id=asset_id)
            except  ObjectDoesNotExist as e:
                print(e)
            return render(request, 'assets/asset_detail.html', {'asset_obj': asset_obj})
        else:
            asset_obj = models.Assets.objects.filter(id=asset_id).values()[0]
            server_obj = models.Server.objects.filter(assets_id=asset_id).values()[0]
            data=dict(asset_obj, **server_obj)
            if data['idc_id'] is None:
                idc = '未分配'
            else:
                idc = models.IDC.objects.filter(id=data['idc_id']).values('name')[0]

            print(idc)
            data['idc_id'] = idc
            print(data)
            json_data = json.dumps(data,cls=CJsonEncoder)
            return HttpResponse(json_data)


def asset_category(request, type):
    assets = asset_handle.fetch_asset_list(type)
    obj = models.Assets.objects.all()
    data = pages(request, obj, 10)
    print(obj)
    return render(request, 'assets/asset.html', {'assets': assets, 'posts': data})
    # return HttpResponse('hahaha')


def assets_approval(request):
    if request.method == 'GET':
        type = 'approved'
        assets = asset_handle.fetch_asset_list(type)
        obj = models.Assets.objects.all().filter(approved=False)
        data = pages(request, obj, 10)
        return render(request, 'assets/assets_approval.html', {'asset_data': assets, 'posts': data})
    else:
        id_list = request.POST.getlist('ids[]')
        print('id_list', id_list)
        obj_list = models.Assets.objects.filter(id__in=id_list).update(approved=True)
        print(obj_list)
        return HttpResponse('ok')


def create_assets(args):
    data = json.loads(args.body.decode())

    print(data)
    for k, v in data.items():
        asset_info = {
            'sn': v['assets_sn'],
            # 'memo': v['data'],
            'name': v['hostname'],
            'assets_type': v['assets_type'],

        }
        print('创建数据', asset_info)
        asset_already_in_approval_zone = models.Assets.objects.get_or_create(**asset_info)


def update_server(args):
    data = json.loads(args.decode())

    server_info = {
        'assets_id': models.Assets.objects.get(sn=str(data.get('assets_sn'))).id,
        'ip': '10.10.30.222',
        'cpu': data.get('cpu_model'),
        'cpu_number': data.get('cpu_count'),
        'cpu_core': data.get('cpu_core_count'),
        'disk_total': '1024',
        'ram_capacity': data.get('ram_size'),
        'raid': '5',
        'os_type': data.get('os_type'),
        'os_distribution': data.get('os_distribution'),
        'os_release': data.get('os_release'),
        'model': data.get('model'),
        'manufactory_id': models.Manufactory.objects.get(manufactory=data.get('manufactory')).id,

    }
    print('更新数据', server_info)
    asset_server = models.Server.objects.update_or_create(
            assets_id=models.Assets.objects.get(sn=str(data.get('assets_sn'))).id, defaults=server_info)


def asset_report(request):
    '''
    判断是资产入库还是更新资产
    :param request:
    :return:
    '''
    if request.method == 'POST':
        data = json.loads((request.body).decode())
        print(data)

        for k, v in data.items():
            print(k, v)

            asset_info = {
                'sn': v['assets_sn'],
                # 'memo': v['data'],
                'name': v['hostname'],
                'assets_type': v['assets_type'],

            }
            sn = models.Assets.objects.update_or_create(sn=v['assets_sn'], defaults=asset_info)
            server_info = {
                'assets_id': models.Assets.objects.get(sn=v['assets_sn']).id,
                'ip': v['ip'],
                'cpu': v['cpu_model'][2],
                'cpu_number': v['cpu_count'],
                'cpu_core': v['cpu_core_count'],
                'disk_total': v['disk_count'],
                'ram_capacity': v['ram_size'],
                'raid': '5',
                'os_type': v['os_type'],
                'os_distribution': v['os_distribution'],
                'os_release': v['os_release'],
                'model': v['model'],
                'manufactory_id': models.Manufactory.objects.get(manufactory=v['manufactory']).id,

            }
            if v['assets_type'] == 'server':
                print('更新数据', server_info)
            asset_server = models.Server.objects.update_or_create(
                    assets_id=models.Assets.objects.get(sn=v['assets_sn']).id, defaults=server_info)

            #
        return HttpResponse('--数据汇报完毕--')

    return HttpResponse('--test--')
