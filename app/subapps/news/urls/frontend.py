#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django.conf.urls import url

from ..views.frontend import *

urlpatterns = [
    url(r'^lista_aktualnosci$', NoticesListView.as_view(),
        name='notices_list_view'),
    url(r'^szukaj$', SearchNoticesView.as_view(), name='search_notices_view'),
    url(r'^(?P<notice_id>[\d]+)$', NoticeView.as_view(), name='notice_view'),
]