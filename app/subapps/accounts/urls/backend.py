#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django.conf.urls import url

from ..views.backend import *

urlpatterns = [
    url(r'^lista_uzytkownikow$', UsersListView.as_view(),
        name='users_list_view'),
    url(r'^szukaj$', SearchUsersView.as_view(), name='search_users_view'),
    url(r'^uzytkownik/(?P<user_id>[\d]+)$', ShowUserProfileView.as_view(),
        name='show_user_profile_view'),
    url(r'^zmien_status_uzytkownika/(?P<user_id>[\d]+)$',
        ChangeUserStatusView.as_view(), name='change_user_status_view'),
    url(r'dodaj_uzytkownika', AddUserView.as_view(), name='add_user_view')
]
