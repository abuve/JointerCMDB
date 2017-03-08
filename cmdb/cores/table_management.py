__author__ = 'buhe'

import xlwt
import xlrd
import os
import datetime
import random

from cmdb import models as cmdb_models
from cmdb.cores import asset_num

FILE_PATH = './upload/cmdb'


class TableUpdate:
    def __init__(self):
        self.file_name = str(int(datetime.datetime.now().strftime("%Y%m%d%H%M%S")) + random.randint(10, 99)) + '.xls'
        self.col_name = ['机房', 'IP', '主机名称', '资产编号', 'SN', '资产类型', '厂商', '型号', '位置信息', '配置信息',
                         '运维人', '使用人', '业务部门', '资产属性', '备注']

    def __handle_upload_file(self, f):
        try:
            destination = open('%s/%s' % (FILE_PATH, self.file_name), 'wb')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
            return True
        except Exception as e:
            print(Exception, e)
            return False

    # 文件校验函数
    def __handle_table(self):
        try:
            file_data = xlrd.open_workbook('%s/%s' % (FILE_PATH, self.file_name))
            table = file_data.sheets()[0]
            for i in range(0, table.ncols):
                if table.col_values(i)[0] != self.col_name[i]:
                    return {'code': 1, 'msg': '提示：表格数据不规范，导入失败。'}
            return {'code': 0}
        except Exception as e:
            print(Exception, e)
            return {'code': 1, 'msg': '提示：文件格式错误，请检查!'}

    # 数据库更新函数
    def __handle_update(self):
        file_data = xlrd.open_workbook('%s/%s' % (FILE_PATH, self.file_name))
        table = file_data.sheets()[0]
        table_dic = {}
        # 临时IP列表，用于存放更新失败的IP地址
        false_ip_list = []
        count = 0
        for row in range(0, table.nrows):
            for col in range(0, table.ncols):
                if row == 0:
                    continue
                else:
                    # 更新数据
                    table_dic[self.col_name[col]] = table.row_values(row)[col]

            if table_dic:
                try:
                    get_update_object = cmdb_models.Asset.objects.get(asset_num=table_dic['资产编号'])
                except:
                    get_update_object = None

                if get_update_object:
                    get_update_object.idc = cmdb_models.IDC.objects.get(name=table_dic['机房'])
                    get_update_object.nic_set.all().update(ipaddress=table_dic['IP'])
                    get_update_object.name = table_dic['主机名称']
                    get_update_object.server.sn = table_dic['SN']
                    get_update_object.asset_type = table_dic['资产类型']
                    if table_dic['厂商']:
                        get_update_object.manufactory = cmdb_models.Manufactory.objects.get(manufactory=table_dic['厂商'])
                    get_update_object.server.model = table_dic['型号']
                    get_update_object.server.configuration = table_dic['配置信息']
                    get_update_object.admin = table_dic['运维人']
                    get_update_object.user = table_dic['使用人']
                    get_update_object.dept = table_dic['业务部门']
                    get_update_object.memo = table_dic['备注']
                    get_update_object.server.save()
                    get_update_object.save()
                    for i in get_update_object.nic_set.all():
                        print(i.ipaddress)
                else:
                    get_asset_num = asset_num.asset_num_builder()
                    try:
                        new_asset_data = cmdb_models.Asset(
                            name=table_dic['主机名称'],
                            asset_num=get_asset_num,
                            idc=cmdb_models.IDC.objects.get(name=table_dic['机房']),
                            admin=table_dic['运维人'],
                            user=table_dic['使用人'],
                            dept=table_dic['业务部门'],
                            memo=table_dic['备注'],
                        )

                        if table_dic['厂商']:
                            new_asset_data.manufactory = cmdb_models.Manufactory.objects.get(manufactory=table_dic['厂商'])

                        new_asset_data.save()

                        new_server_data = cmdb_models.Server(
                            asset=new_asset_data,
                            created_by='excel',
                            sn=table_dic['SN'],
                        )
                        new_server_data.save()

                        new_nic_data = cmdb_models.NIC(
                            asset=new_asset_data,
                            ipaddress=table_dic['IP'],
                        )
                        new_nic_data.save()

                    except Exception as e:
                        print(Exception, e)
                        pass
        return 1

    def main(self, post_file):
        # 定义表格列名规范，后续可配置数据库
        file_upload = self.__handle_upload_file(post_file)
        if file_upload:
            check = self.__handle_table()
            if check['code'] == 0:
                # 执行更新入库
                self.__handle_update()

        return 1