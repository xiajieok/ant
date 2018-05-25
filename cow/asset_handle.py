import json
import sys
import os

from cow import models


def fetch_asset_list(args):
    if args == 'all':
        objs = models.Assets.objects.all()
    elif args == 'approved':
        objs = models.Assets.objects.filter(approved=False)
    else:
        objs = models.Assets.objects.filter(assets_type=args).filter(approved=True)

    res_list = []
    for obj in objs:
        if obj.assets_type == 'server':
            try:
                cpu_model = obj.cpu.cpu_model
                cpu_core_count = obj.cpu.cpu_core_count
            except Exception as e:
                cpu_model = None
                cpu_core_count = None
            data = {
                'sn': obj.sn,
                'name': obj.name,
                'id': obj.id,
                'idc': None if not obj.idc else obj.idc.name,
                'business_unit': None if not obj.business_unit else obj.business_unit.name,
                # 'manufactory': None if not obj.manufactory else obj.manufactory.manufactory,
                # 'model': get_asset_model(obj),
                'cpu_model': cpu_model,
                'cpu_core_count': cpu_core_count,
                'asset_type': obj.get_assets_type_display(),
                'management_ip': obj.management_ip,
                # 'ram_size': format(float(obj.mem_total / 1024), '.2f'),
                # 'disk_size': obj.disk_total,
                # 'tags': obj.tags.name,
                'status': obj.get_status_display(),
                'update_date': obj.update_date,
                # 'cabinet': None if not obj.cabinet else obj.cabinet.name,
            }
            # print(data)
        else:
            data = {
                'sn': obj.sn,
                'name': obj.name,
                'id': obj.id,
                'idc': None if not obj.idc else obj.idc.name,
                'business_unit': None if not obj.business_unit else obj.business_unit.name,
                # 'manufactory': None if not obj.manufactory else obj.manufactory.manufactory,
                # 'model': get_asset_model(obj),
                'asset_type': obj.get_assets_type_display(),
                'management_ip': obj.management_ip,
                # 'ram_size': format(float(obj.mem_total / 1024), '.2f'),
                # 'disk_size': obj.disk_total,
                # 'tags': obj.tags.name,
                'status': obj.get_status_display(),
                'update_date': obj.update_date,
                # 'cabinet': None if not obj.cabinet else obj.cabinet.name,
            }
        res_list.append(data)
    return {'data': res_list}
