#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django.conf.urls import url

from ..views.backend import (
    MetersListView, MeterDataView, DeleteMeterView, EditMeterDataView,
    ChangeMeterUsersView)

urlpatterns = [
    url(r'^lista_licznikow$', MetersListView.as_view(),
        name='meters_list_view'),
    url(r'^dane_licznika/(?P<meter_id>[\d]+)$', MeterDataView.as_view(),
        name='meters_details_view'),
    url(r'^usun_licznik/(?P<meter_id>[\d]+)$', DeleteMeterView.as_view(),
        name='delete_meter_view'),
    url(r'^edytuj_dane_licznika/(?P<meter_id>[\d]+)$',
        EditMeterDataView.as_view(), name='edit_meter_view'),
    url(r'^edytuj_liste_wlascicieli/(?P<meter_id>[\d]+)$',
        ChangeMeterUsersView.as_view(), name='change_meter_owners_view'),
]
