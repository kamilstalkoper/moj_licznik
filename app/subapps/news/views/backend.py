#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django.db.models import Q
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.utils.html import escape
from django.views.generic import ListView, FormView, UpdateView

from .frontend import NoticeView, BreakdownsListView, BreakdownView
from ..forms import CreateNoticeForm, CreateBreakdownForm
from ..models import Notice, Breakdown


class BackendNoticesListView(ListView):
    context_object_name = 'notices'
    http_method_names = [u'get', ]
    model = Notice
    page_kwarg = 'strona'
    paginate_by = 10
    template_name = 'backend/news/notices_list.html'

    search_phrase = None

    def get(self, request, *args, **kwargs):
        self.search_phrase = escape(request.GET.get('q', ''))
        return super(BackendNoticesListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BackendNoticesListView, self).get_context_data(**kwargs)
        if not self.search_phrase:
            return context

        context.update({
            'is_searched': True,
            'search_phrase': self.search_phrase,
        })
        return context

    def get_queryset(self):
        qs = Notice.objects.all().order_by('-created_at')
        if not self.search_phrase:
            return qs

        return qs.filter(
            Q(title__icontains=self.search_phrase) |
            Q(content_body__icontains=self.search_phrase))


class CreateNoticeView(FormView):
    form_class = CreateNoticeForm
    http_method_names = [u'post', u'get']
    template_name = 'backend/news/create_notice.html'

    def form_valid(self, form):
        form.save()
        return redirect('backend:backend_notices_list_view')


class EditNoticeView(UpdateView):
    form_class = CreateNoticeForm
    http_method_names = [u'post', u'get']
    pk_url_kwarg = 'notice_id'
    model = Notice
    template_name = 'backend/news/create_notice.html'
    success_url = '/backend/aktualnosci/lista_aktualnosci'


class BackendNoticeView(NoticeView):
    template_name = 'backend/news/notice.html'

    def get_queryset(self):
        return Notice.objects \
            .all() \
            .prefetch_related('breakdowns', 'breakdowns__stations')


class BackendBreakdownsListView(BreakdownsListView):
    http_method_names = [u'get', ]
    template_name = 'backend/news/breakdowns_list.html'

    def get_queryset(self):
        return Breakdown.objects.all().order_by('-start_at')


class BackendBreakdownView(BreakdownView):
    template_name = 'backend/news/breakdown.html'


class CreateBreakdownView(FormView):
    form_class = CreateBreakdownForm
    http_method_names = [u'post', u'get']
    template_name = 'backend/news/create_breakdown.html'

    def form_valid(self, form):
        form.save()
        return redirect('backend:backend_breakdowns_list_view')


class EditBreakdownView(UpdateView):
    form_class = CreateBreakdownForm
    http_method_names = [u'post', u'get']
    pk_url_kwarg = 'breakdown_id'
    model = Breakdown
    template_name = 'backend/news/create_breakdown.html'
    success_url = '/backend/aktualnosci/lista_wylaczen'
