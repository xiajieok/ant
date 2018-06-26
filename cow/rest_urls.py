#_*_coding:utf-8_*_
__author__ = 'xxx'
from django.conf.urls import url, include
from rest_framework import routers
from cow import rest_views as views
from cow import views as cow_views
router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
router.register(r'assets', views.AssetViewSet)
router.register(r'idcs', views.IDCViewSet)
router.register(r'business', views.BusinessUnitSet)


# from cow import rest_test
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    # url(r'asset_list/$',views.AssetList ),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^dashboard_data/',cow_views.get_dashboard_data,name="get_dashboard_data"),
    # url(r'^eventlogs/$', rest_test.eventlog_list),
]