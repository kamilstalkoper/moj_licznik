#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django.conf.urls import url

from ..views.frontend import *

urlpatterns = [
    # meters management
    url(r'^moje_liczniki$', MetersListView.as_view(), name='meters_list_view'),
    url(r'^usun_licznik/(?P<meter_id>[\d]+)$', RemoveMeterView.as_view(),
        name='remove_meter'),
    url(r'^dodaj_licznik$', AddMeterView.as_view(), name='add_meter'),
    url(r'^licznik/(?P<meter_id>[\d]+)$', MeterDataView.as_view(),
        name='meter_data_view'),
    url(r'^ustaw_jako_glowny$', SetMeterAsMainView.as_view(),
        name='set_as_main_view'),
    url(r'^zmien_alias/(?P<meter_id>[\d]+)$', ChangeMeterAliasView.as_view(),
        name='change_meter_alias_view'),

    # alarms
    url(r'^moje_alarmy$', AlarmsListView.as_view(), name='alarms_list_view'),
    url(r'^alarm/(?P<alarm_id>[\d]+)$', AlarmDetailsView.as_view(),
        name='alarm_details_view'),
    url(r'^dodaj_alarm$', AddAlarmView.as_view(), name='add_alarm_view'),
    url(r'^edytuj_alarm/(?P<alarm_id>[\d]+)$', EditAlarmView.as_view(),
        name='edit_alarm_view'),
    url(r'^usun_alarm/(?P<alarm_id>[\d]+)$', DeleteAlarmView.as_view(),
        name='delete_alarm_view'),
]
