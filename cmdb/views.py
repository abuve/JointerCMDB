from django.shortcuts import render, render_to_response, HttpResponse

# Create your views here.
from cmdb.cores import query_data
from cmdb.cores import table_management
from cmdb.cores import modify_management
from cmdb import models as CMDB_MODELS

import json
import time
import os


def index(request):
    return render_to_response('main.html')


def main(request):
    return render_to_response('workbench.html')


def test1(request):
    return render_to_response('test1.html')


'''def get_data(request):

    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start_with = (page - 1) * rows
    end_with = page * rows
    total_count = len(UserData.objects.all())
    get_data_from_db = UserData.objects.values()[start_with:end_with]
    data_list = []
    for items in get_data_from_db:
        data_list.append(items)
    return_data = {"total": total_count, 'rows': data_list}
    return HttpResponse(json.dumps(return_data))'''


def get_data_by_id(request):
    rows_id = request.POST.get('id')
    get_data_from_db = UserData.objects.filter(id=rows_id).values()
    data_list = []
    for items in get_data_from_db:
        data_list.append(items)
    print(json.dumps(data_list))
    return HttpResponse(json.dumps(data_list))


def add(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')

    update_data = UserData(
        username=username,
        password=password,
        email=email
    )
    update_data.save()

    return HttpResponse(1)


def edit(request):
    print(request.POST)
    id_edit = int(request.POST.get('id_edit'))
    password_edit = request.POST.get('password_edit')
    email_edit = request.POST.get('email_edit')

    try:
        get_update_data = UserData.objects.get(id=id_edit)
        print(get_update_data)
    except Exception as e:
        print(Exception, e)
        return HttpResponse(0)

    get_update_data.password = password_edit
    get_update_data.email = email_edit
    get_update_data.save()

    return HttpResponse(1)


def delete(request):
    id_delete = request.POST.getlist('id_delete')
    for row_id in id_delete:
        get_delete_data = UserData.objects.get(id=row_id)
        get_delete_data.delete()

    return HttpResponse(1)


def get_data(request):
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    search_items = json.loads(request.POST.get('search_items'))

    search_obj = query_data.QueryMain(page, rows)

    for search_object in search_items:
        search_func = getattr(search_obj, 'search_by_%s' % search_object['tag'])
        source_data = search_func(search_object['operator'], search_object['value'])

    return HttpResponse(json.dumps(source_data))


def search_data(request):
    return HttpResponse(1)


def upload(request):
    post_file = request.FILES['file']
    upload_obj = table_management.TableUpdate()
    upload_obj.main(post_file)
    return HttpResponse(1)


def manager_data_edit(request):
    get_edit_data = json.loads(request.POST.get('edit_data'))
    manager_update = modify_management.AssetUpdate(get_edit_data)
    manager_update.sql_update()
    return HttpResponse(1)


def get_server_detail(request):
    object_id = request.POST.get('object_id')
    get_asset_data = CMDB_MODELS.Asset.objects.get(id=object_id)
    return_data = {
        'result': get_asset_data
    }
    return render_to_response('cmdb-server-detail.html', return_data)


def get_idc_all(request):
    idc_all = CMDB_MODELS.IDC.objects.values()
    data_list = []
    for items in idc_all:
        data_list.append(items)

    idc_all_str = json.dumps(data_list)

    '''for i in CMDB_MODELS.Asset.objects.all():
        i.delete()'''

    return HttpResponse(idc_all_str)


def get_asset_type_all(request):
    asset_type_all = CMDB_MODELS.Asset.asset_type_choices
    data_list = []
    for item in asset_type_all:
        data_list.append({'asset_value': item[0], 'asset_name': item[1]})

    asset_type_all_str = json.dumps(data_list)

    return HttpResponse(asset_type_all_str)


def get_manufactory_all(request):
    manufactory_all = CMDB_MODELS.Manufactory.objects.values()
    data_list = []
    for items in manufactory_all:
        data_list.append(items)

    return HttpResponse(json.dumps(data_list))


def management(request):
    return render_to_response('cmdb-management.html')


def management_idc(request):
    return render_to_response('cmdb-management-idc.html')


def get(request):
    return render_to_response('cmdb-management-idc.html')