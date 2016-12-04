#!/usr/bin/env python
# encoding: utf-8

from django.conf.urls import url, include

from .views import *

urlpatterns = [
    # dashboard
    url(r'^$', BackendDashboardView.as_view(), name='dashboard'),

    # backend accounts
    url(r'^konta/', include('app.subapps.accounts.urls.backend'))
]
