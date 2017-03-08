from django.contrib import admin

# Register your models here.

from cmdb import models as cmdb_models

# admin.site.register(UserData)

'''
配置Django后台admin数据编辑显示
'''
class ServerInline(admin.TabularInline):
    model = cmdb_models.Server
    exclude = ('memo',)
    readonly_fields = ['create_date']


class CPUInline(admin.TabularInline):
    model = cmdb_models.CPU
    exclude = ('memo',)
    readonly_fields = ['create_date']


class NICInline(admin.TabularInline):
    model = cmdb_models.NIC
    exclude = ('memo',)
    readonly_fields = ['create_date']


class RAMInline(admin.TabularInline):
    model = cmdb_models.RAM
    exclude = ('memo',)
    readonly_fields = ['create_date']


class DiskInline(admin.TabularInline):
    model = cmdb_models.Disk
    exclude = ('memo',)
    readonly_fields = ['create_date']


'''
定制后台数据加载项
'''
class AssetAdmin(admin.ModelAdmin):
    list_display = ('id', 'asset_type', 'name', 'manufactory')
    search_fields = ['sn', ]
    inlines = [ServerInline, CPUInline, RAMInline, DiskInline, NICInline]
    list_filter = ['manufactory', 'asset_type']

class IDCAdmin(admin.ModelAdmin):
    list_display = ('name', )

'''
加载数据
'''
admin.site.register(cmdb_models.Asset, AssetAdmin)
admin.site.register(cmdb_models.Server)
admin.site.register(cmdb_models.IDC, IDCAdmin)
admin.site.register(cmdb_models.Manufactory)

admin.site.register(cmdb_models.CPU)
admin.site.register(cmdb_models.RAM)
admin.site.register(cmdb_models.Disk)
admin.site.register(cmdb_models.NIC)
admin.site.register(cmdb_models.FieldManagement)