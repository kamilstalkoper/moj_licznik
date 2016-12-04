#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django.conf.urls import url

from ..views.frontend import *

urlpatterns = [
    url(r'^moje_liczniki$', MetersListView.as_view(), name='meters_list_view'),
    url(r'^usun_licznik/(?P<meter_id>[\d]+)$', RemoveMeterView.as_view(),
        name='remove_meter'),
    url(r'^dodaj_licznik$', AddMeterView.as_view(), name='add_meter'),
    url(r'^licznik/(?P<meter_id>[\d]+)$', MeterDataView.as_view(),
        name='meter_data_view'),
    url(r'^zmien_licznik_glowny$', MainMeterChangeView.as_view(),
        name='main_meter_change_view'),
    url(r'^ustaw_jako_glowny$', SetMeterAsMainView.as_view(),
        name='set_as_main_view'),
]
