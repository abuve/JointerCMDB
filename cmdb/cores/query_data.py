__author__ = 'buhe'


from cmdb import models as cmdb_models


class QueryMain:
    def __init__(self, page=1, limit=10):
        self.page = int(page)
        self.limit = int(limit)
        self.start_tag = self.page * self.limit - self.limit
        self.end_tag = self.page * self.limit
        self.cmdb_data = cmdb_models.Asset.objects

    def __get_field_data(self):
        pass

    def __page_data_calculator(self):
        pass

    def __formatting_json(self, source_data):
        items_list = []
        for objects in source_data:
            items_data = {}
            items_data['id'] = objects.id
            items_data['asset_num'] = objects.asset_num
            items_data['idc'] = objects.idc.name

            try:
                items_data['ip'] = objects.nic_set.all()[0].ipaddress
            except:
                items_data['ip'] = 'unknow'

            try:
                items_data['sn'] = objects.server.sn
            except:
                items_data['sn'] = '未知'

            items_data['asset_type'] = objects.asset_type

            try:
                items_data['manufactory'] = objects.manufactory.manufactory
            except:
                items_data['manufactory'] = '未知'

            items_data['model'] = objects.server.model
            items_data['os_type'] = objects.server.os_type
            items_data['os_version'] = objects.server.os_release
            items_data['position'] = 'E3-18-01'

            '''items_data['cpu'] = objects.cpu.cpu_model
            items_data['mem'] = objects.ram_set.all()[0].capacity
            items_data['disk'] = objects.disk_set.all()[0].capacity'''

            items_data['cpu_used'] = '30%'
            items_data['mem_used'] = '28%'
            items_data['disk_used'] = '45%'

            items_data['configuration'] = objects.server.configuration

            items_data['admin'] = objects.admin
            items_data['user'] = objects.user
            items_data['use_dept'] = objects.dept

            items_list.append(items_data)

        formatting_data = {
            'total': len(self.cmdb_data),
            'rows': items_list
        }

        return formatting_data

    def search_by_default(self, operator, value):
        self.cmdb_data = self.cmdb_data.all()
        source_data = self.cmdb_data.order_by('-id')[self.start_tag: self.end_tag]
        return_search_data = self.__formatting_json(source_data)
        return return_search_data

    def search_by_ip(self, operator, value):
        if operator == 'exact':
            self.cmdb_data = self.cmdb_data.filter(nic__ipaddress=value)
            source_data = self.cmdb_data.order_by('-id')[self.start_tag: self.end_tag]
        elif operator == 'like':
            self.cmdb_data = self.cmdb_data.filter(nic__ipaddress__contains=value)
            source_data = self.cmdb_data.order_by('-id')[self.start_tag: self.end_tag]

        return_search_data = self.__formatting_json(source_data)

        return return_search_data

    def search_by_idc(self, operator, value):
        if operator == 'exact':
            self.cmdb_data = self.cmdb_data.filter(idc__name=value)
            source_data = self.cmdb_data.order_by('-id')[self.start_tag: self.end_tag]
        elif operator == 'like':
            self.cmdb_data = self.cmdb_data.filter(idc__name__contains=value)
            source_data = self.cmdb_data.order_by('-id')[self.start_tag: self.end_tag]

        return_search_data = self.__formatting_json(source_data)

        return return_search_data

    def search_by_admin(self, operator, value):
        if operator == 'exact':
            self.cmdb_data = self.cmdb_data.filter(admin=value)
            source_data = self.cmdb_data.order_by('-id')[self.start_tag: self.end_tag]
        elif operator == 'like':
            self.cmdb_data = self.cmdb_data.filter(admin__contains=value)
            source_data = self.cmdb_data.order_by('-id')[self.start_tag: self.end_tag]

        return_search_data = self.__formatting_json(source_data)

        return return_search_data

    def search_by_user(self, operator, value):
        if operator == 'exact':
            self.cmdb_data = self.cmdb_data.filter(user=value)
            source_data = self.cmdb_data.order_by('-id')[self.start_tag: self.end_tag]
        elif operator == 'like':
            self.cmdb_data = self.cmdb_data.filter(user__contains=value)
            source_data = self.cmdb_data.order_by('-id')[self.start_tag: self.end_tag]

        return_search_data = self.__formatting_json(source_data)

        return return_search_data