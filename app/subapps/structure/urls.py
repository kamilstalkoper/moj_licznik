#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home_view'),
]
