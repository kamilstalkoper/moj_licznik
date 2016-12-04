#!/usr/bin/env python
# encoding: utf-8

from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    # django admin panel
    url(r'^admin/', admin.site.urls),

    # accounts
    url(r'^rejestracja/', include('app.subapps.accounts.urls.registration',
                                  namespace='registration')),
    url(r'^konto/', include('app.subapps.accounts.urls.accounts',
                                  namespace='accounts')),
    url(r'^zarzadzaj_licznikami/',
        include('app.subapps.accounts.urls.meter_management',
                namespace='meter_management')),

    # authentication
    url(r'^', include('app.subapps.accounts.urls.registration',
                      namespace='authentication')),

    # contact
    url(r'^kontakt/', include('app.subapps.contact.urls', namespace='contact')),

    # news
    url(r'^aktualnosci/', include('app.subapps.news.urls.frontend',
                                  namespace='news')),

    # structure
    url(r'^', include('app.subapps.structure.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
