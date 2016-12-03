#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django.conf.urls import url
from django.contrib.auth.views import password_change, password_change_done

from django.contrib.auth.forms import PasswordChangeForm

from ..views.accounts import *

urlpatterns = [
    # profile
    url(r'^$', ProfileView.as_view(), name='profile_view'),
    url(r'^edytuj_dane$', EditUserDataView.as_view(),
        name='edit_user_data_view'),

    # password change
    url(r'^zmien_haslo$', password_change,
        {
            'template_name': 'accounts/password_change.html',
            'post_change_redirect': 'accounts:password_change_done',
        },
        name='password_change'),
    url(r'^haslo_zostalo_zmienione$', password_change_done,
        {'template_name': 'accounts/password_change_done.html'},
        name='password_change_done'),
]
