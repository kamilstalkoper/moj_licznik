#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django.conf.urls import url

from ..views.backend import *

urlpatterns = [
    # news
    url(r'^lista_aktualnosci$', BackendNoticesListView.as_view(),
        name='backend_notices_list_view'),
    url(r'^(?P<notice_id>[\d]+)$', BackendNoticeView.as_view(),
        name='backend_notice_view'),
    url(r'^nowa_aktualnosc$', CreateNoticeView.as_view(),
        name='create_notice_view'),
    url(r'^edycja_aktualnosci/(?P<notice_id>[\d]+)$', EditNoticeView.as_view(),
        name='edit_notice_view'),

    # breakdowns
    url(r'^lista_wylaczen$', BackendBreakdownsListView.as_view(),
        name='backend_breakdowns_list_view'),
    url(r'^wylaczenie/(?P<breakdown_id>[\d]+)$', BackendBreakdownView.as_view(),
        name='backend_breakdown_view'),
    url(r'^nowe_wylaczenie$', CreateBreakdownView.as_view(),
        name='create_breakdown_view'),
    url(r'^edycja_wylaczenia/(?P<breakdown_id>[\d]+)$',
        EditBreakdownView.as_view(), name='edit_breakdown_view'),
]
