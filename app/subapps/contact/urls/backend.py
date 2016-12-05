#!/usr/bin/env python
# encoding: utf-8

from django.conf.urls import url

from ..views.backend import *

urlpatterns = [
    url(r'^lista_wiadomosci$', BackendProblemsView.as_view(),
        name='backend_problems_view'),
    url(r'^nowa_wiadomosc/(?P<user_id>[\d]+)$', BackendNewProblemView.as_view(),
        name='backend_new_problem_view'),
    url(r'^wiadomosci_w_watku/(?P<problem_id>[\d]+)$',
        BackendProblemMessagesView.as_view(),
        name='backend_problem_messages_view'),
    url(r'^odpowiedz/(?P<problem_id>[\d]+)$',
        BackendSendMessageView.as_view(), name='backend_send_message_view'),
    url(r'^set_as_solved$', BackendSetAsSolvedView.as_view(),
        name='backend_set_as_solved')
]
