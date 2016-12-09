#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.db.models import Max
from django.shortcuts import get_object_or_404, Http404, redirect
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator

from .frontend import (
    SetAsSolvedView, ProblemsView, NewProblemView, ProblemMessagesView)
from ..models import Problem, Message


@method_decorator(staff_member_required(login_url='authentication:auth_login'),
                  name='dispatch')
class BackendProblemsView(ProblemsView):
    template_name = 'backend/contact/problems_list.html'

    def get_queryset(self):
        return Problem.objects \
            .all() \
            .annotate(last_message=Max('message__created_at')) \
            .order_by('solved', '-last_message')


@method_decorator(staff_member_required(login_url='authentication:auth_login'),
                  name='dispatch')
class BackendNewProblemView(NewProblemView):
    template_name = 'backend/contact/new_problem.html'
    user = None

    def get(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, id=kwargs.get('user_id'))
        return super(BackendNewProblemView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, id=kwargs.get('user_id'))
        return super(BackendNewProblemView, self).post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(BackendNewProblemView, self).get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def redirect(self):
        return redirect('backend:backend_problems_view')

    def send_email_to_user(self, content, electrician_needed):
        context = {
            'electrician_needed': electrician_needed,
            'content': content,
        }
        message = render_to_string(
            'contact/email/message_content.html', context)
        send_mail(
            subject='Nowa wiadomość od administartora serwisu '
                    'mojLicznik.pl',
            message=message,
            from_email=settings.SERVER_EMAIL,
            recipient_list=[self.user.email, ]
        )


@method_decorator(staff_member_required(login_url='authentication:auth_login'),
                  name='dispatch')
class BackendProblemMessagesView(ProblemMessagesView):
    template_name = 'backend/contact/problem_messages_list.html'

    def get_queryset(self):
        return Message.objects \
            .filter(problem_id=self.problem_id) \
            .order_by('-created_at')


@method_decorator(staff_member_required(login_url='authentication:auth_login'),
                  name='dispatch')
class BackendSendMessageView(BackendNewProblemView):
    http_method_names = [u'post', ]

    problem = None

    def post(self, request, *args, **kwargs):
        self.problem = Problem.objects \
            .filter(id=kwargs.get('problem_id')).first()
        if self.problem is None:
            raise Http404
        return super(BackendSendMessageView, self).post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(BackendSendMessageView, self).get_form_kwargs()
        kwargs['problem'] = self.problem
        return kwargs

    def redirect(self):
        return redirect('backend:backend_problem_messages_view',
                        problem_id=self.problem.id)

    def form_invalid(self, form):
        return self.redirect()


@method_decorator(staff_member_required(login_url='authentication:auth_login'),
                  name='dispatch')
class BackendSetAsSolvedView(SetAsSolvedView):
    default_redirect_view = 'backend:'
    admin_action = True
