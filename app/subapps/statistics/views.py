#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import ShowMeterDataForm

from app.subapps.structure.models import UserMeterPoint


@method_decorator(login_required, name='dispatch')
class MainStatisticsView(FormView):
    http_method_names = [u'get', u'post']
    form_class = ShowMeterDataForm
    template_name = 'statistics/main_statistics.html'

    def get_form_kwargs(self):
        kwargs = super(MainStatisticsView, self).get_form_kwargs()
        user_meter_point = UserMeterPoint.objects \
            .filter(user_id=self.request.user.id, is_main_meter_point=True) \
            .last()
        kwargs['main_meter_point'] = user_meter_point.meter_point \
            if user_meter_point is not None else None
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(MainStatisticsView, self).get_context_data(**kwargs)
        if not UserMeterPoint.objects \
                .filter(user_id=self.request.user.id, is_main_meter_point=True)\
                .exists():
            context['main_meter_error'] = u'Wybierz lucznik główny na górze ' \
                                          u'strony i sprubój jeszcze raz!'
        return context

    def form_valid(self, form):
        context = self.get_context_data(**self.kwargs)
        if form.main_meter_point is not None:
            context = form.get_meter_data()
            context['form'] = form
        return self.render_to_response(context)
