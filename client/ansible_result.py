import json
import os
import requests
import re
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
            disk = facts['ansible_devices'],
            disk_data = {}
            # print(disk)
            # print(type(disk))
            for i, j in disk[0].items():
                print(i)
                tmp = re.findall(r"^[s|v]d[a-z]", i)
                if len(tmp) >= 1:
                    disk_data[i] = j['size']
            if facts['ansible_product_serial'] == 'NA':
                assets_sn = facts['ansible_product_uuid']
            else:
                assets_sn = facts['ansible_product_serial']
            # print(facts)
            res = {
                "hostname": facts['ansible_hostname'],
                "ip": facts['ansible_all_ipv4_addresses'],
                "ram_size": facts['ansible_memtotal_mb'] // 1024,
                "ram_free": facts['ansible_memfree_mb'],
                "cpu_model": facts['ansible_processor'],
                "cpu_count": facts['ansible_processor_vcpus'],
                "disk_count": disk_data,
                # "cpu_core_count": len(facts['ansible_processor']),
                "cpu_core_count": facts['ansible_processor_vcpus'],
                "system_type": facts['ansible_system'],
                # "os_distribution": facts['ansible_distribution'],
                "os_distribution": facts['ansible_distribution_version'],
                "uuid": facts['ansible_product_uuid'],
                "model": facts['ansible_product_name'],
                "os_type": facts['ansible_system'],
                "os_release": facts['ansible_distribution'],
                # "asset_sn": facts['ansible_product_serial'],
                "assets_sn": assets_sn,
                'assets_type': 'server',
                'manufactory': facts['ansible_system_vendor']
            }
            data[k] = res
            # JSON = json.dumps(res)
            print(res)
        return data


class SendInfo(object):
    def __init__(self, data):
        self.data = data
        pass

    def new(self):
        data = self.data
        for k, v in data.items():
            uuid = v['uuid']
            print(uuid)
            #     pass
            id_file = os.path.join(os.getcwd(), '.asset_id')
            # if os.path.exists(id_file) is True:
            #     id = open(id_file, 'r').read()
            #     return id
            # else:
            with open(id_file, 'a+') as f:
                info = uuid + '\n'
                f.write(info)
                # pass

    def post_data(self):
        # data = self.data
        # data['id'] = self.get_id()
        url = 'http://ant.91jyy.com/asset/asset_report/'
        res = requests.post(url, self.data)
        return res


if __name__ == '__main__':
    msg = Normal().info()
    # print('全部数据', data)
    # print(type(data))
    jsondata = json.dumps(msg)
    # data = {'192.168.1.176': {'os_release': 'Dell Inc.', 'ram_free': 138486, 'ip': ['192.168.122.1', '192.168.1.176'], 'hostname': 'dev', 'system_type': 'Linux', 'ram_size': 157, 'assets_sn': 'ASDAEWQDQWEQWE', 'uuid': '44454C4C-3100-1058-8031-C3C04F533632', 'os_type': 'PowerEdge R730', 'cpu_model': ['0', 'GenuineIntel', 'Intel(R) Xeon(R) CPU E5-2609 v3 @ 1.90GHz', '1', 'GenuineIntel', 'Intel(R) Xeon(R) CPU E5-2609 v3 @ 1.90GHz', '2', 'GenuineIntel', 'Intel(R) Xeon(R) CPU E5-2609 v3 @ 1.90GHz', '3', 'GenuineIntel', 'Intel(R) Xeon(R) CPU E5-2609 v3 @ 1.90GHz', '4', 'GenuineIntel', 'Intel(R) Xeon(R) CPU E5-2609 v3 @ 1.90GHz', '5', 'GenuineIntel', 'Intel(R) Xeon(R) CPU E5-2609 v3 @ 1.90GHz', '6', 'GenuineIntel', 'Intel(R) Xeon(R) CPU E5-2609 v3 @ 1.90GHz', '7', 'GenuineIntel', 'Intel(R) Xeon(R) CPU E5-2609 v3 @ 1.90GHz', '8', 'GenuineIntel', 'Intel(R) Xeon(R) CPU E5-2609 v3 @ 1.90GHz', '9', 'GenuineIntel', 'Intel(R) Xeon(R) CPU E5-2609 v3 @ 1.90GHz', '10', 'GenuineIntel', 'Intel(R) Xeon(R) CPU E5-2609 v3 @ 1.90GHz', '11', 'GenuineIntel', 'Intel(R) Xeon(R) CPU E5-2609 v3 @ 1.90GHz'], 'manufactory': 'kvm', 'assets_type': 'server', 'cpu_count': 12, 'cpu_core_count': '4', 'os_distribution': 'CentOS'}, '192.168.1.174': {'os_release': 'Red Hat', 'ram_free': 30862, 'ip': ['192.168.1.174', '172.17.42.1'], 'hostname': 'db', 'system_type': 'Linux', 'ram_size': 31, 'assets_sn': 'ASDAEWQDQWEQWE', 'uuid': '2459AD74-1D0A-43F1-B53E-2A9910CDC6E5', 'os_type': 'KVM', 'cpu_model': ['0', 'GenuineIntel', 'Intel Xeon E312xx (Sandy Bridge)', '1', 'GenuineIntel', 'Intel Xeon E312xx (Sandy Bridge)'], 'manufactory': 'kvm', 'assets_type': 'server', 'cpu_count': 2, 'cpu_core_count': '4', 'os_distribution': 'CentOS'}}
    res = SendInfo(data=jsondata).post_data()
