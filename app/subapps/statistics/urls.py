#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django.conf.urls import url

from .views import MainStatisticsView

urlpatterns = [
    url(r'^$', MainStatisticsView.as_view(), name='main_statistics_view')
]