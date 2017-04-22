"""ChennaiLoco URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from train import views as v

urlpatterns = [
    url(r'^$', v.home_view, name='home'),
    url(r'^auth/$', v.auth_view, name='auth'),
    url(r'^register/$', v.register_view, name='register'),
    url(r'^trains/$', v.train_list.as_view(), name='trains'),
    url(r'^train/(?P<pk>\d{1,6})/$', v.train_view, name='train'),
    url(r'^stations/$', v.station_list.as_view(), name='stations'),
    url(r'^station/(?P<slug>[\w-]+)/$', v.station_view, name='station'),
    url(r'^station/(?P<slug>[\w-]+)/review$', v.review_view, name='review'),
    url(r'^search/$', v.search_view, name='search'),
    url(r'^search/train/$', v.train_search_view, name='trainsearch'),
    url(r'^search/station/$', v.station_search_view, name='stationsearch'),
    url(r'^search/place/$', v.places_search_view, name='placessearch'),
    url(r'^api/trains/$', v.train_api.as_view(), name='trainapi'),
    url(r'^api/stations/$', v.station_api.as_view(), name='stationapi'),
]
