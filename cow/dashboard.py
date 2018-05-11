from cow import models
from django.db.models import Count
import random


class AssetDashboard(object):
    '''
    统计资产信息，统计设备数量，取出子类型name
    :return  返回格式 {"asset_categories": {"data": [2, 1], "names": ["PC\u670d\u52a1\u5668", "\u8def\u7531\u5668"]}}

    '''

    def __init__(self, request):
        self.request = request
        self.asset_list = models.Assets.objects.all()
        self.data = {}

    def searilize_page(self):
        self.data['asset_categories'] = self.get_asset_categories()
        self.data['asset_status'] = self.get_asset_status()
        self.data['business_load'] = self.get_business_load()

    def get_asset_categories(self):
        '''按资产类型进行分类'''

        dataset = {
            'names': [],
            'data': []
        }
        # 设置一个字典，格式为{ 设备类型：数量}
        prefetch_data = {
            models.Assets: None,
            # models.NetworkDevice: None,
            # models.SecurityDevice: None,
            # models.Software: None,
        }
        for key in prefetch_data:
            '''
            循环字典的key,将资产类型聚合统计出各资产的总数，生成列表【{资产类型：总数}】
            '''
            data_list = list(key.objects.values('assets_type').annotate(total=Count('assets_type')))
            for index, category in enumerate(data_list):
                '''
                循环各类型设备的子类型，判断type是否相等，如果相等，就取出来这个子类型，塞给data_list
                '''
                for db_val, display_name in key.assets_type_choices:
                    if category['assets_type'] == db_val:
                        data_list[index]['name'] = display_name
            for item in data_list:
                '''
                循环data_list 将取到的子类型name和统计结果添加到 dataset
                注意此处 name 和 data是固定格式，不可更改
                '''
                dataset['names'].append(item['name'])
                dataset['data'].append(item['total'])
        # prefetch_data[key] = data_list
        return dataset

    def get_asset_status(self):
        queryset = list(self.asset_list.values('status').annotate(value=Count('status')))
        dataset = {
            'names': [],
            'data': [],
        }
        for index, item in enumerate(queryset):
            print(index, item)
            for db_val, display_name in models.Assets.status_choices:
                if db_val == item['status']:
                    queryset[index]['name'] = display_name
                    if db_val == 0:
                        queryset[index]['itemStyle'] = {
                            'normal': {'color': 'yellowgreen'}
                        }
                        # for item in queryset:
                        # print(item['name'])
        dataset['names'] = [item['name'] for item in queryset]
        dataset['value'] = queryset
        return dataset

    def get_business_load(self):
        dataset = {
            'names': [],
            'data': {'load': [], 'left': []}  # left是为了填充百分比用的
        }
        # for obj in models.BusinessUnit.objects.filter(parent_level=None):
        for obj in models.BusinessUnit.objects.all():
            load_val = random.randint(1, 100)  # 这是个模拟数据，模拟各业务线的使用率负载
            dataset['names'].append(obj.name)
            dataset['data']['load'].append(load_val)
            dataset['data']['left'].append(100 - load_val)
        print('business load ', dataset)
        return dataset

# print("prefecth data",prefetch_data)
# print("dataset",dataset)
