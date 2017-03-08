from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class UserData(models.Model):
    username = models.CharField(u'用户名称', max_length=40)
    password = models.CharField(u'用户密码', max_length=40)
    email = models.CharField(u'用户邮箱', max_length=40)
    # create_date = models.DateTimeField(blank=True, auto_now_add=True)


class Asset(models.Model):
    asset_type_choices = (
        ('server', u'物理机'),
        ('docker', u'Docker'),
    )
    asset_type = models.CharField(choices=asset_type_choices, max_length=64, default='server')
    name = models.CharField(max_length=64, null=True, blank=True)
    asset_num = models.CharField(u'资产编号', max_length=128, unique=True)
    idc = models.ForeignKey('IDC', verbose_name=u'IDC机房')
    manufactory = models.ForeignKey('Manufactory', verbose_name=u'制造商', null=True, blank=True)
    admin = models.CharField(max_length=20)
    user = models.CharField(max_length=20)
    dept = models.CharField(max_length=100)
    memo = models.TextField(u'备注', null=True, blank=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, auto_now=True)

    def __unicode__(self):
        return 'id:%s name:%s' % (self.id, self.name)

    class Meta:
        verbose_name = '资产总表'
        verbose_name_plural = "资产总表"


class Manufactory(models.Model):
    manufactory = models.CharField(u'厂商名称', max_length=64, unique=True)
    support_num = models.CharField(u'支持电话', max_length=30,blank=True)
    memo = models.CharField(u'备注',max_length=128,blank=True)

    def __unicode__(self):
        return self.manufactory

    class Meta:
        verbose_name = '厂商'
        verbose_name_plural = "厂商"


class IDC(models.Model):
    name = models.CharField(u'机房名称', max_length=64, unique=True)
    en_name = models.CharField(u'英文名称', max_length=64, unique=True, null=True, blank=True)
    position = models.CharField(u'机房位置', max_length=64, unique=True, null=True, blank=True)
    phone = models.CharField(u'支持电话', max_length=64, unique=True, null=True, blank=True)
    memo = models.CharField(u'备注', max_length=128, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '机房'
        verbose_name_plural = "机房"


class Server(models.Model):
    asset = models.OneToOneField("Asset")
    created_by_choices = (
        ('auto', 'Auto'),
        ('manual', 'Manual'),
        ('excel', 'Excel'),
    )
    created_by = models.CharField(choices=created_by_choices, max_length=32, default='auto')
    hosted_on = models.ForeignKey('self', related_name='hosted_on_server', blank=True, null=True)
    sn = models.CharField(u'SN号', max_length=128, blank=True, null=True)
    management_ip = models.CharField(u'管理IP',max_length=64, blank=True, null=True)
    model = models.CharField(u'型号', max_length=128, null=True, blank=True)
    raid_type = models.CharField(u'raid类型', max_length=512, blank=True, null=True)
    configuration = models.CharField(u'硬件配置', max_length=100, blank=True, null=True)
    os_type = models.CharField(u'系统类型', max_length=64, blank=True, null=True)
    os_distribution = models.CharField(u'发型版本', max_length=64, blank=True, null=True)
    os_release = models.CharField(u'系统版本', max_length=64, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = "服务器"

    def __unicode__(self):
        return '%s' % (self.asset.name)


class CPU(models.Model):
    asset = models.OneToOneField('Asset')
    cpu_model = models.CharField(u'CPU型号', max_length=128, blank=True)
    cpu_count = models.SmallIntegerField(u'物理cpu个数')
    cpu_core_count = models.SmallIntegerField(u'cpu核数')
    memo = models.TextField(u'备注', null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'CPU部件'
        verbose_name_plural = "CPU部件"

    def __unicode__(self):
        return self.cpu_model


class RAM(models.Model):
    asset = models.ForeignKey('Asset')
    sn = models.CharField(u'SN号', max_length=128, blank=True,null=True)
    model = models.CharField(u'内存型号', max_length=128)
    slot = models.CharField(u'插槽', max_length=64)
    capacity = models.IntegerField(u'内存大小(MB)')
    memo = models.CharField(u'备注',max_length=128, blank=True,null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'RAM'
        verbose_name_plural = "RAM"
        unique_together = ("asset", "slot")

    def __unicode__(self):
        return '%s:%s:%s' % (self.asset_id, self.slot, self.capacity)


class Disk(models.Model):
    asset = models.ForeignKey('Asset')
    sn = models.CharField(u'SN号', max_length=128, blank=True,null=True)
    slot = models.CharField(u'插槽位',max_length=64)
    manufactory = models.CharField(u'制造商', max_length=64,blank=True,null=True)
    model = models.CharField(u'磁盘型号', max_length=128,blank=True,null=True)
    capacity = models.FloatField(u'磁盘容量GB')
    disk_iface_choice = (
        ('SATA', 'SATA'),
        ('SAS', 'SAS'),
        ('SCSI', 'SCSI'),
        ('SSD', 'SSD'),
    )
    iface_type = models.CharField(u'接口类型', max_length=64,choices=disk_iface_choice,default='SAS')
    memo = models.TextField(u'备注', blank=True, null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ("asset", "slot")
        verbose_name = '硬盘'
        verbose_name_plural = "硬盘"

    def __unicode__(self):
        return '%s:slot:%s capacity:%s' % (self.asset_id,self.slot,self.capacity)


class NIC(models.Model):
    asset = models.ForeignKey('Asset')
    name = models.CharField(u'网卡名', max_length=64, blank=True,null=True)
    sn = models.CharField(u'SN号', max_length=128, blank=True,null=True)
    model = models.CharField(u'网卡型号', max_length=128, blank=True, null=True)
    macaddress = models.CharField(u'MAC', max_length=64, blank=True, null=True)
    ipaddress = models.GenericIPAddressField(u'IP', blank=True, null=True)
    netmask = models.CharField(max_length=64, blank=True, null=True)
    bonding = models.CharField(max_length=64, blank=True, null=True)
    memo = models.CharField(u'备注', max_length=128, blank=True,null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True,null=True)

    class Meta:
        unique_together = ("asset", "name")
        verbose_name = u'网卡'
        verbose_name_plural = u"网卡"

    def __unicode__(self):
        return '%s:%s' % (self.asset_id, self.macaddress)


class FieldManagement(models.Model):
    field_type_choices = (
        ('server', u'服务器'),
        ('switch', u'交换机'),
        ('router', u'路由器'),
        ('firewall', u'防火墙'),
        ('storage', u'存储设备'),
        ('NLB', u'NetScaler'),
        ('wireless', u'无线AP'),
        ('software', u'软件资产'),
        ('others', u'其它类'),
    )
    field_type = models.CharField(choices=field_type_choices, max_length=64, default='server')
    field_list = models.CharField(u'字段列表', max_length=2000, blank=True,null=True)
    memo = models.CharField(u'备注', max_length=128, blank=True,null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = u'字段管理'
        verbose_name_plural = u"字段管理"

    def __unicode__(self):
        return self.field_type
