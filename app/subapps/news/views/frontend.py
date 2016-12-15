#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.views.generic import ListView, DetailView

from ..models import Notice, Breakdown


@method_decorator(login_required, name='dispatch')
class NoticesListView(ListView):
    context_object_name = 'notices'
    http_method_names = [u'get', ]
    model = Notice
    page_kwarg = 'strona'
    paginate_by = 10
    template_name = 'news/notices_list.html'

    def get_queryset(self):
        return Notice.objects \
            .filter(Q(users__isnull=True) | Q(users=self.request.user)) \
            .order_by('-created_at')


@method_decorator(login_required, name='dispatch')
class SearchNoticesView(NoticesListView):
    search_phrase = None

    def get(self, request, *args, **kwargs):
        self.search_phrase = escape(request.GET.get('q', ''))
        return super(SearchNoticesView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SearchNoticesView, self).get_context_data(**kwargs)
        if not self.search_phrase:
            return context

        context.update({
            'is_searched': True,
            'search_phrase': self.search_phrase,
        })
        return context

    def get_queryset(self):
        qs = super(SearchNoticesView, self).get_queryset()
        if not self.search_phrase:
            return qs

        return qs.filter(
            Q(title__icontains=self.search_phrase) |
            Q(content_body__icontains=self.search_phrase))


@method_decorator(login_required, name='dispatch')
class NoticeView(DetailView):
    context_object_name = 'notice'
    http_method_names = [u'get', ]
    model = Notice
    pk_url_kwarg = 'notice_id'
    template_name = 'news/notice.html'

    def get_queryset(self):
        return Notice.objects \
            .filter(Q(users__isnull=True) | Q(users=self.request.user)) \
            .prefetch_related('breakdowns', 'breakdowns__stations')


@method_decorator(login_required, name='dispatch')
class BreakdownsListView(ListView):
    context_object_name = 'breakdowns'
    http_method_names = [u'get', ]
    model = Breakdown
    page_kwarg = 'strona'
    paginate_by = 10
    template_name = 'news/breakdowns_list.html'

    def get_queryset(self):
        return Breakdown.objects \
            .filter(stations__meterpoint__users=self.request.user) \
            .order_by('-start_at')


@method_decorator(login_required, name='dispatch')
class BreakdownView(DetailView):
    context_object_name = 'breakdown'
    http_method_names = [u'get', ]
    model = Breakdown
    pk_url_kwarg = 'breakdown_id'
    template_name = 'news/breakdown.html'

    def get_queryset(self):
        return Breakdown.objects \
            .all() \
            .prefetch_related('stations') \
            .order_by('-start_at')
