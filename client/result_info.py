# coding:utf-8
import json
import os
import requests
from collections import namedtuple
from ansible import constants as C

from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display

    display = Display()


class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """

    def __init__(self, *args, **kwargs):
        # super(ResultsCollector, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.host_failed[result._host.get_name()] = result


class CMDjob(object):
    def __init__(self, hosts, host_list, module, args, ssh_user='root', passwords='null', ack_pass=False, forks=5,
                 ext_vars=None):
        self.loader = DataLoader()
        self.inventory = InventoryManager(loader=self.loader, sources=[hosts])  # ../conf/hosts是定义hosts
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        self.hosts = hosts
        self.host_list = host_list
        self.ssh_user = ssh_user
        self.passwords = dict(vault_pass=passwords)
        self.loader = DataLoader()
        self.ack_pass = ack_pass
        self.forks = forks
        self.module = module
        self.args = args
        # self.inventory = InventoryManager(loader=loader, sources=[self.hosts])  # ../conf/hosts是定义hosts
        # self.variable_manager = VariableManager(loader=loader, inventory=inventory)
        # 初始化需要的对象
        self.Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'timeout', 'remote_user',
                                              'ask_pass', 'private_key_file', 'ssh_common_args', 'ssh_extra_args',
                                              'sftp_extra_args',
                                              'scp_extra_args', 'become', 'become_method', 'become_user',
                                              'ask_value_pass',
                                              'verbosity', 'diff', 'check', 'listhosts', 'listtasks', 'listtags',
                                              'syntax'])
        self.options = self.Options(connection='smart',
                                    module_path='/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/site-packages/ansible/modules',
                                    forks=5, become=None, become_method=None, become_user="root", remote_user='root',
                                    ask_pass=False,
                                    private_key_file=None, ssh_common_args=None, ssh_extra_args=None, timeout=10,
                                    sftp_extra_args=None, scp_extra_args=None, check=False, diff=False,
                                    ask_value_pass=False, verbosity=None, listhosts=False,
                                    listtasks=False, listtags=False, syntax=False)

        # self.run()

    def run(self):
        # 创建任务
        play_source = dict(
                name="Ansible Play",
                hosts=self.host_list,
                gather_facts='no',
                tasks=[
                    dict(action=dict(module=self.module, args=self.args), register='shell_out'),
                    # 定义一条任务，如有多条任务也应按照这样的方式定义
                ]
        )
        # print(play_source)
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)
        tqm = None
        results_callback = ResultCallback()

        tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=self.passwords,
                stdout_callback=results_callback,

        )
        result = tqm.run(play)
        results_raw = {}
        results_raw['success'] = {}
        results_raw['failed'] = {}
        results_raw['unreachable'] = {}

        for host, result in results_callback.host_ok.items():
            results_raw['success'][host] = json.dumps(result._result)

        for host, result in results_callback.host_failed.items():
            results_raw['failed'][host] = result._result['msg']

        for host, result in results_callback.host_unreachable.items():
            results_raw['unreachable'][host] = result._result['msg']
        return results_raw


class Normal(object):
    '''
    检查服务器信息,返回json数据

    '''

    def __init__(self, hosts, host_list, module, args):
        self.hosts = hosts
        self.host_list = host_list
        self.module = module
        self.args = args
        # self.info()

    def info(self):
        msg = CMDjob(hosts=self.hosts,
                     host_list=self.host_list,
                     module=self.module,
                     args=self.args,
                     ).run()
        facts = dict(json.loads(msg['success']['10.10.30.102']))['ansible_facts']
        res = {
            "hostname": facts['ansible_hostname'],
            "ip": facts['ansible_all_ipv4_addresses'],
            "ram_size": facts['ansible_memtotal_mb']//1024,
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
            "asset_sn": 'ASDAEWQDQWEQWE',
            'asset_type':'server'
        }
        JSON = json.dumps(res)
        # print(JSON)
        return res


class SendInfo(object):
    def __init__(self, data):
        self.data = msg
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
    msg = Normal(hosts='hosts',
                 host_list='km',
                 module='setup',
                 args=' ',
                 ).info()
    # print(msg)
    res = SendInfo(data=msg).post_data()
    print(res)
    # host = '10.10.30.100'
    # with open('ansible_client.json') as f:
    #     msg = json.loads(f.read())
    #
    # facts = msg[host]['ansible_facts']
    # hostname = facts['ansible_hostname']
    # ip = facts['ansible_all_ipv4_addresses']
    # memtotal = facts['ansible_memtotal_mb']
    # memfree = facts['ansible_memfree_mb']
    # cpu_processor = facts['ansible_processor']
    # cpu_processor_num = facts['ansible_processor_vcpus']
    #
    # system_type = facts['ansible_system']
    # system_distribution = facts['ansible_distribution']
    # uuid = facts['ansible_product_uuid']
    # product_name = facts['ansible_product_name']
    # product_vendor = facts['ansible_system_vendor']
    # sn = facts['ansible_product_serial']
    #
    # print(sn)
