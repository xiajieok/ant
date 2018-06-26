from django.db import models


# Create your models here.
class Assets(models.Model):
    assets_type_choices = (
        ('server', u'服务器'),
        ('switch', u'交换机'),
        ('route', u'路由器'),
        ('printer', u'打印机'),
        ('scanner', u'扫描仪'),
        ('firewall', u'防火墙'),
        ('storage', u'存储设备'),
        ('wifi', u'无线设备'),
    )
    assets_type = models.CharField(choices=assets_type_choices, max_length=100, default='server', verbose_name='资产类型')
    name = models.CharField(max_length=100, verbose_name='主机名', unique=True)
    sn = models.CharField(max_length=100, verbose_name='设备序列号')
    buy_time = models.DateField(blank=True, null=True, verbose_name='购买时间')
    expire_date = models.DateField(u'过保修期', null=True, blank=True)
    management_ip = models.GenericIPAddressField(u'管理IP', blank=True, null=True)
    # model = models.CharField(max_length=100, blank=True, null=True, verbose_name='资产型号')
    # put_zone = models.SmallIntegerField(blank=True, null=True, verbose_name='放置区域')
    business_unit = models.ForeignKey('BusinessUnit', verbose_name=u'所属业务线', null=True, blank=True,
                                      on_delete=models.SET_NULL)
    tags = models.ManyToManyField('Tag', blank=True)
    # admin = models.ForeignKey('UserProfile', verbose_name=u'资产管理员', null=True, blank=True,on_delete=models.SET_NULL)
    idc = models.ForeignKey('IDC', verbose_name=u'IDC机房', null=True, blank=True, on_delete=models.SET_NULL)

    status_choices = ((0, '在线'),
                      (1, '下线'),
                      (2, '未知'),
                      (3, '故障'),
                      (4, '备用'),
                      )
    status = models.SmallIntegerField(choices=status_choices, default=0)
    # Configuration = models.OneToOneField('Configuration',verbose_name='配置管理',blank=True,null=True)

    memo = models.TextField(u'备注', null=True, blank=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, auto_now=True)
    approved = models.BooleanField(u'已批准', default=False)

    class Meta:
        verbose_name = '资产总表'
        verbose_name_plural = "资产总表"


class Server(models.Model):
    assets = models.OneToOneField('Assets', on_delete=models.SET_NULL, null=True)
    sub_assset_type_choices = (
        (0, 'PC服务器'),
        (1, '刀片机'),
        (2, '小型机'),
    )
    created_by_choices = (
        ('auto', 'Auto'),
        ('manual', 'Manual'),
    )
    ip = models.CharField(max_length=100, unique=True, blank=True, null=True)
    # username = models.CharField(max_length=100, blank=True, null=True)
    # passwd = models.CharField(max_length=100, blank=True, null=True)
    # keyfile = models.SmallIntegerField(blank=True,
    #                                    null=True)  # FileField(upload_to = './upload/key/',blank=True,null=True,verbose_name='密钥文件')
    # port = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True)
    # line = models.CharField(max_length=100, blank=True, null=True)
    cpu = models.CharField(u'CPU型号', max_length=100, blank=True, null=True)
    cpu_number = models.SmallIntegerField(u'CPU颗数', blank=True, null=True)
    cpu_core = models.SmallIntegerField(u'CPU核数', blank=True, null=True)
    disk_total = models.CharField(u'磁盘', max_length=100, blank=True, null=True)
    ram_capacity = models.CharField(u'内存', max_length=100, blank=True, null=True)
    # selinux = models.CharField(max_length=100, blank=True, null=True)
    # swap = models.CharField(max_length=100, blank=True, null=True)
    raid = models.SmallIntegerField(u'Raid型号', blank=True, null=True)
    os_type = models.CharField(u'操作系统类型', max_length=64, blank=True, null=True)
    os_distribution = models.CharField(u'发型版本', max_length=64, blank=True, null=True)
    os_release = models.CharField(u'操作系统版本', max_length=64, blank=True, null=True)
    manufactory = models.ForeignKey('Manufactory', verbose_name=u'制造商', null=True, blank=True,
                                    on_delete=models.SET_NULL)
    model = models.CharField(verbose_name=u'型号', max_length=128, null=True, blank=True)
    contract = models.ForeignKey('Contract', verbose_name=u'合同', null=True, blank=True, on_delete=models.SET_NULL)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        # db_table = 'opman_server_assets'
        # permissions = (
        #     ("can_read_server_assets", "读取服务器资产权限"),
        #     ("can_change_server_assets", "更改服务器资产权限"),
        #     ("can_add_server_assets", "添加服务器资产权限"),
        #     ("can_delete_server_assets", "删除服务器资产权限"),
        # )
        verbose_name = '服务器'
        verbose_name_plural = '服务器'


class Manufactory(models.Model):
    """厂商"""

    manufactory = models.CharField(u'厂商名称', max_length=64, unique=True)
    support_num = models.CharField(u'支持电话', max_length=30, blank=True)
    memo = models.CharField(u'备注', max_length=128, blank=True)

    def __str__(self):
        return self.manufactory

    class Meta:
        verbose_name = '厂商'
        verbose_name_plural = "厂商"


class BusinessUnit(models.Model):
    """业务线"""

    # parent_unit = models.ForeignKey('self', related_name='parent_level', blank=True, null=True,
    #                                 on_delete=models.SET_NULL)
    name = models.CharField(u'业务线', max_length=64, unique=True)

    # contact = models.ForeignKey('UserProfile',default=None)
    memo = models.CharField(u'备注', max_length=64, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '业务线'
        verbose_name_plural = "业务线"


class Contract(models.Model):
    """合同"""

    sn = models.CharField(u'合同号', max_length=128, unique=True)
    name = models.CharField(u'合同名称', max_length=64)
    memo = models.TextField(u'备注', blank=True, null=True)
    price = models.IntegerField(u'合同金额')
    detail = models.TextField(u'合同详细', blank=True, null=True)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    license_num = models.IntegerField(u'license数量', blank=True)
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    class Meta:
        verbose_name = '合同'
        verbose_name_plural = "合同"

    def __str__(self):
        return self.name


class IDC(models.Model):
    """机房"""

    name = models.CharField(u'机房名称', max_length=64, unique=True,default='阿里云')
    memo = models.CharField(u'备注', max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '机房'
        verbose_name_plural = "机房"


class Tag(models.Model):
    """资产标签"""

    name = models.CharField('Tag name', max_length=32, unique=True)
    # creator = models.ForeignKey('UserProfile',on_delete=models.SET_NULL)
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = "标签"


class EventLog(models.Model):
    """事件"""

    name = models.CharField(u'事件名称', max_length=100)
    event_type_choices = (
        (1, u'硬件变更'),
        (2, u'新增配件'),
        (3, u'设备下线'),
        (4, u'设备上线'),
        (5, u'定期维护'),
        (6, u'业务上线\更新\变更'),
        (7, u'其它'),
    )
    event_type = models.SmallIntegerField(u'事件类型', choices=event_type_choices)
    asset = models.ForeignKey('Assets', on_delete=models.SET_NULL, null=True)
    component = models.CharField('事件子项', max_length=255, blank=True, null=True)
    detail = models.TextField(u'事件详情')
    date = models.DateTimeField(u'事件时间', auto_now_add=True)
    # user = models.ForeignKey('UserProfile', verbose_name=u'事件源')
    memo = models.TextField(u'备注', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '事件纪录'
        verbose_name_plural = "事件纪录"

    def colored_event_type(self):
        if self.event_type == 1:
            cell_html = '<span style="background: orange;">%s</span>'
        elif self.event_type == 2:
            cell_html = '<span style="background: yellowgreen;">%s</span>'
        else:
            cell_html = '<span >%s</span>'
        return cell_html % self.get_event_type_display()

    colored_event_type.allow_tags = True
    colored_event_type.short_description = u'事件类型'
