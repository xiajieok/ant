"""ant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from cow import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^', include('cow.urls')),
    # url(r'^$', views.index, name="index"),
    url(r'^api/', include('cow.rest_urls') ),
    url(r'^category/(.+)?/$', views.asset_category, name="category"),
    url(r'^list/(\d+)/$', views.asset_detail, name="detail"),
    url(r'^assets_approval/$', views.assets_approval, name="approval"),
    url(r'^new_asset/$', views.asset_with_no_asset_id, name="new_asset"),
    url(r'^asset_report/$', views.asset_report, name="asset_report"),
]
