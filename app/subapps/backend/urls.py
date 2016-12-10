#!/usr/bin/env python
# encoding: utf-8

from django.conf.urls import url, include

from .views import *

urlpatterns = [
    # dashboard
    url(r'^$', BackendDashboardView.as_view(), name='dashboard'),

    # backend accounts
    url(r'^konta/', include('app.subapps.accounts.urls.backend')),

    # backend contact
    url(r'^kontakt/', include('app.subapps.contact.urls.backend')),

    # backend news
    url(r'^aktualnosci/', include('app.subapps.news.urls.backend')),

    # backend meters management
    url(r'^zarzadzanie_licznikami/',
        include('app.subapps.meters_management.urls.backend')),
]
