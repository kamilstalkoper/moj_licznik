#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Max
from django.shortcuts import get_object_or_404, Http404, redirect
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView, ListView

from ..forms import NewMessageForm
from ..models import Problem, Message


@method_decorator(login_required, name='dispatch')
class ProblemsView(ListView):
    context_object_name = 'problems'
    http_method_names = [u'get', ]
    model = Problem
    page_kwarg = 'strona'
    paginate_by = 10
    template_name = 'contact/problems_list.html'

    def get_queryset(self):
        return Problem.objects \
            .filter(user_id=self.request.user.id) \
            .annotate(last_message=Max('message__created_at')) \
            .order_by('solved', '-last_message')


@method_decorator(login_required, name='dispatch')
class NewProblemView(FormView):
    form_class = NewMessageForm
    http_method_names = [u'post', u'get']
    template_name = 'contact/new_problem.html'

    def get_form_kwargs(self):
        kwargs = super(NewProblemView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def redirect(self):
        return redirect('contact:problems_view')

    def form_valid(self, form):
        form.save()
        if form.cleaned_data.get('send_copy_to_me'):
            self.send_email_to_user(
                form.cleaned_data.get('message_content'),
                form.cleaned_data.get('electrician_needed')
            )
        return self.redirect()

    def send_email_to_user(self, content, electrician_needed):
        context = {
            'electrician_needed': electrician_needed,
            'content': content,
        }
        message = render_to_string(
            'contact/email/message_content.html', context)
        send_mail(
            subject='Wiadomość wysłana do administartora serwisu '
                    'mojLicznik.pl',
            message=message,
            from_email=settings.SERVER_EMAIL,
            recipient_list=[self.request.user.email, ]
        )


@method_decorator(login_required, name='dispatch')
class ProblemMessagesView(ListView):
    allow_empty = False
    context_object_name = 'messages'
    http_method_names = [u'get', ]
    model = Message
    page_kwarg = 'strona'
    paginate_by = 10
    template_name = 'contact/problem_messages_list.html'

    problem_id = None

    def get_context_data(self, **kwargs):
        context = super(ProblemMessagesView, self).get_context_data(**kwargs)
        context['problem_id'] = self.problem_id
        context['problem_solved'] = Problem.objects.filter(
            id=self.problem_id, solved=False).exists()
        return context

    def get(self, request, *args, **kwargs):
        self.problem_id = kwargs.get('problem_id')
        return super(ProblemMessagesView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return Message.objects\
            .filter(problem__user_id=self.request.user.id,
                    problem_id=self.problem_id).order_by('-created_at')


@method_decorator(login_required, name='dispatch')
class SendMessageView(NewProblemView):
    http_method_names = [u'post', ]

    problem = None

    def post(self, request, *args, **kwargs):
        self.problem = Problem.objects.filter(
            user_id=self.request.user.id, id=kwargs.get('problem_id')).first()
        if self.problem is None:
            raise Http404
        return super(SendMessageView, self).post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(SendMessageView, self).get_form_kwargs()
        kwargs['problem'] = self.problem
        return kwargs

    def redirect(self):
        return redirect('contact:problem_messages_view',
                        problem_id=self.problem.id)

    def form_invalid(self, form):
        return redirect('contact:problems_view',
                        problem_id=self.problem.id)


@method_decorator(login_required, name='dispatch')
class SetAsSolvedView(TemplateView):
    http_method_names = [u'post', ]

    default_redirect_view = 'contact:problems_view'
    admin_action = False

    def post(self, request, *args, **kwargs):
        redirect_to = request.POST.get('redirect_to')
        problem_id = request.POST.get('problem_id', '')

        try:
            problem_id = int(problem_id)
        except ValueError:
            raise Http404

        problem = get_object_or_404(Problem.objects.select_related('user'),
                                    id=problem_id, solved=False)

        problem.solved = True
        problem.save()
        self.send_email_to_user(problem)

        if not redirect_to:
            return redirect(self.default_redirect_view)

        return redirect(redirect_to)

    def send_email_to_user(self, problem):
        context = {
            'problem': problem,
            'admin_action': self.admin_action,
        }
        message = render_to_string(
            'backend/contact/email/problem_solved_message.html', context)
        send_mail(
            subject='Problem został uznany za rozwiązany.',
            message=message,
            from_email=settings.SERVER_EMAIL,
            recipient_list=[problem.user.email, ]
        )
