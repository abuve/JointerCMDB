"""JointerServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from cmdb import views as cmdb_views

urlpatterns = [
    url(r'^index/', cmdb_views.index),
    url(r'^main/', cmdb_views.main),
    url(r'^test1/', cmdb_views.test1),
    url(r'^add/', cmdb_views.add),
    url(r'^edit/', cmdb_views.edit),
    url(r'^delete/', cmdb_views.delete),
    url(r'^get_data_by_id/', cmdb_views.get_data_by_id),
    url(r'^get_data/', cmdb_views.get_data),
    url(r'^search_data/', cmdb_views.search_data),
    url(r'^upload/', cmdb_views.upload),
    url(r'^manager_data_edit/', cmdb_views.manager_data_edit),
    url(r'^get_server_detail/', cmdb_views.get_server_detail),
    url(r'^get_idc_all/', cmdb_views.get_idc_all),
    url(r'^get_asset_type_all/', cmdb_views.get_asset_type_all),
    url(r'^get_manufactory_all/', cmdb_views.get_manufactory_all),
    url(r'^management/$', cmdb_views.management),
    url(r'^management/idc/$', cmdb_views.management_idc),
]