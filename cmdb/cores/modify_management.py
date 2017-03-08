__author__ = 'buhe'


from cmdb import models as CMDB_MODELS


class AssetUpdate:
    def __init__(self, update_json):
        self.source_update_json = update_json
        self.asset_object_from_db = CMDB_MODELS.Asset
        self.asset_update = None
        self.update_field = ['idc', 'asset_type', 'manufactory', 'admin', 'user', 'use_dept']

    def update_idc(self, value):
        if value != self.asset_update.idc.name:
            get_idc_from_db = CMDB_MODELS.IDC.objects.get(name=value)
            self.asset_update.idc = get_idc_from_db

    def update_asset_type(self, value):
        if value != self.asset_update.asset_type:
            self.asset_update.asset_type = value

    def update_manufactory(self, value):
        try:
            get_current_manufactory = self.asset_update.manufactory.manufactory
        except:
            get_current_manufactory = None

        if value != get_current_manufactory:
            get_manufactory_from_db = CMDB_MODELS.Manufactory.objects.get(manufactory=value)
            self.asset_update.manufactory = get_manufactory_from_db

    def update_admin(self, value):
        if value != self.asset_update.admin:
            self.asset_update.admin = value

    def update_user(self, value):
        if value != self.asset_update.user:
            self.asset_update.user = value

    def update_use_dept(self, value):
        if value != self.asset_update.dept:
            self.asset_update.dept = value

    def sql_update(self):
        for items in self.source_update_json:
            self.asset_update = self.asset_object_from_db.objects.get(id=items['id'])
            for field in self.update_field:
                update_func = getattr(self, 'update_%s' % field)
                update_func(items[field])
            self.asset_update.save()