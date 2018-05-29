import json
import os
import requests
from client.ansible_api import MyRunner

# 传入inventory路径
ansible = MyRunner('./hosts')
# 获取服务器磁盘信息
ansible.run('dev', 'setup', " ")
# 结果
result = ansible.get_result()
# 成功
succ = result['success']
# print(succ)
# 失败
failed = result['failed']
# print(failed)
# 不可到达
unreachable = result['unreachable']


# print(unreachable)

class Normal(object):
    '''
    检查服务器信息,返回json数据

    '''

    def info(self):
        # print(succ)
        data = {}
        for k, v in succ.items():
            # print(k)
            facts = succ[k]['ansible_facts']

            res = {
                "hostname": facts['ansible_hostname'],
                "ip": facts['ansible_all_ipv4_addresses'],
                "ram_size": facts['ansible_memtotal_mb'] // 1024,
                "ram_free": facts['ansible_memfree_mb'],
                "cpu_model": facts['ansible_processor'],
                "cpu_count": facts['ansible_processor_vcpus'],
                "cpu_core_count": '4',
                "system_type": facts['ansible_system'],
                "os_distribution": facts['ansible_distribution'],
                "uuid": facts['ansible_product_uuid'],
                "os_type": facts['ansible_product_name'],
                "os_release": facts['ansible_system_vendor'],
                # "asset_sn": facts['ansible_product_serial'],
                "assets_sn": 'ASDAEWQDQWEQWE',
                'assets_type': 'server',
                'manufactory': facts['ansible_virtualization_type']
            }
            data[k] = res
            # JSON = json.dumps(res)
            # print(res)
        return data


class SendInfo(object):
    def __init__(self, data):
        self.data = data
        pass

    def get_id(self):
        id_file = os.path.join(os.getcwd(), '.asset_id')
        if os.path.exists(id_file) is True:
            id = open(id_file, 'r').read()
            return id
        else:
            # post 请求申请ID
            url = 'http://10.10.30.212:8000/asset/new_asset/'
            id = requests.get(url).content
            with open(id_file, 'w') as f:
                f.write(str(id))
            return id

    def post_data(self):
        data = self.data
        data['id'] = self.get_id()
        url = 'http://10.10.30.212:8000/asset/asset_report/'
        res = requests.post(url, data)
        return res


if __name__ == '__main__':
    msg = Normal().info()
    # print(msg)
    res = SendInfo(data=msg).post_data()
    print(msg)
