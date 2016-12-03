#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django.conf.urls import url

from ..views.meter_management import *

urlpatterns = [
    url(r'^usun_licznik/(?P<meter_id>[\d]+)$', RemoveMeterView.as_view(),
        name='remove_meter'),
    url(r'^dodaj_licznik$', AddMeterView.as_view(), name='add_meter'),
    url(r'^licznik/(?P<meter_id>[\d]+)$', MeterDataView.as_view(),
        name='meter_data_view'),
]
