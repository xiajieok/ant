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
        obj = models.Assets.objects.all()
        data = pages(request, obj, 10)
        print('new', obj)
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
    data = args.POST

    asset_info = {
        'sn': str(data.get('assets_sn')),
        'memo': json.dumps(data),
        'name': data.get('hostname'),
        'assets_type': data.get('assets_type'),

    }
    print('创建数据',asset_info)
    asset_already_in_approval_zone = models.Assets.objects.get_or_create(**asset_info)


def update_server(args):
    data = args.POST

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
    print('更新数据',server_info)
    asset_server = models.Server.objects.update_or_create(
        assets_id=models.Assets.objects.get(sn=str(data.get('assets_sn'))).id, defaults=server_info)


def asset_report(request):
    '''
    判断是资产入库还是更新资产
    :param request:
    :return:
    '''
    if request.method == 'POST':
        data = request.POST
        print(data)
        try:
            print('检查是否存在')
            sn = models.Assets.objects.get(sn=str(data.get('assets_sn')))
        except:
            print('新增数据')
            create_assets(request)
            update_server(request)
        else:
            print('更新数据')
            update_server(request)

        return HttpResponse('--数据汇报完毕--')

    return HttpResponse('--test--')


def asset_with_no_asset_id(request):
    if request.method == 'GET':
        print('开始获取ID')
        res = models.Assets.objects.order_by('-id').values('id')[0:1]
        next_id = int(list(res)[0]['id']) + 1
        print('next ID', next_id)
        return HttpResponse(next_id)
    else:
        data = request.POST
        print(data)
        assets_sn = str(data.get('assets_sn'))
        assets_info = {
            'sn': assets_sn,
            'memo': json.dumps(data),
            'name': data.get('hostname'),
            'manufactory_id': '1',
            'model': 'R720',
            'asset_type': data.get('assets_type'),

        }
        if not models.Assets.objects.filter(sn=assets_sn).values('id'):
            asset_already_in_approval_zone = models.Assets.objects.get_or_create(**assets_sn)
        else:
            new_id = models.Assets.objects.filter(sn=assets_sn).values('id')
            print(new_id)
            for i in new_id:
                for k, v in i.items():
                    obj = {
                        'id': v,
                        'asset_id': v,
                        # 'sub_assset_type': '0',
                        'model': 'R720',
                        'ram_capacity': data.get('ram_size'),
                        'os_type': data.get('system_type'),
                        'os_distribution': str(data.get('os_distribution')),
                        'os_release': str(data.get('os_release')),
                    }
                    asset_server_create = models.Server.objects.update_or_create(**obj)

                    print(asset_server_create)
    return HttpResponse('200')
