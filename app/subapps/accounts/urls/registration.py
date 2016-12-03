#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django.conf.urls import url
from django.contrib.auth.views import (
    login, logout_then_login, password_reset, password_reset_done,
    password_reset_confirm, password_reset_complete)

from ..views.registration import *

urlpatterns = [
    # registration
    url(r'dane_podstawowe$', RegistrationFirstStepView.as_view(),
        name='registration_first_step_view'),
    url(r'dane_uzytkownika/(?P<meter_point_state_id>\d+)$',
        RegistrationSecondStepView.as_view(),
        name='registration_second_step_view'),

    # login
    url(r'^zaloguj$', login, {'template_name': 'registration/login.html'},
        name='auth_login'),
    # logout
    url(r'^wyloguj$', logout_then_login, name='auth_logout'),

    # password reset
    url(r'^przypomnij_haslo$', password_reset,
        {
            'template_name': 'password_reset/reset_password_form.html',
            'email_template_name': 'password_reset/password_reset_email.html',
            'subject_template_name': 'password_reset/password_reset_subject.txt',
            'post_reset_redirect': 'authentication:password_reset_done',
        },
        name='password_reset'),
    url(r'^przymomnienie_hasla_wyslane$', password_reset_done,
        {'template_name': 'password_reset/password_reset_done.html'},
        name='password_reset_done'),
    url(r'^zmien_haslo/(?P<uidb64>[0-9A-Za-z_\-]+)/'
        '(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        password_reset_confirm,
        {
            'template_name': 'password_reset/password_reset_confirm.html',
            'post_reset_redirect': 'authentication:password_reset_complete',
        },
        name='password_reset_confirm'),
    url(r'^zmiana_hasla_zakonczona$', password_reset_complete,
        {'template_name': 'password_reset/password_reset_complete.html'},
        name='password_reset_complete'),
]
