#!/usr/bin/env python
# encoding: utf-8

from django.conf.urls import url

from ..views.frontend import *

urlpatterns = [
    url(r'^lista_watkow$', ProblemsView.as_view(), name='problems_view'),
    url(r'^nowy_watek$', NewProblemView.as_view(), name='new_problem'),
    url(r'^wiadomosci_w_watku/(?P<problem_id>[\d]+)$',
        ProblemMessagesView.as_view(), name='problem_messages_view'),
    url(r'^odpowiedz/(?P<problem_id>[\d]+)$',
        SendMessageView.as_view(), name='send_message_view'),
    url(r'^set_as_solved$', SetAsSolvedView.as_view(), name='set_as_solved')
]
