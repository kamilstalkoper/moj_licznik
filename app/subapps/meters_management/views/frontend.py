#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django.contrib.auth.decorators import login_required
from django.db.models import Max, Min
from django.shortcuts import get_object_or_404, Http404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, DeleteView, FormView, ListView

from app.subapps.structure.models import (
    Alarm, Meter, MeterPoint, MeterData, UserMeterPoint)

from ..forms import (
    AddAlarmForm, AddMeterForm, ChangeMainMeterForm, ChangeMeterAliasForm)


@method_decorator(login_required, name='dispatch')
class MetersListView(ListView):
    context_object_name = 'meters'
    http_method_names = [u'get', ]
    model = Meter
    page_kwarg = 'strona'
    paginate_by = 10
    template_name = 'meter_management/meters_list.html'

    def get_queryset(self):
        return Meter.objects \
            .filter(meterpointstate__meter_point__users=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(MetersListView, self).get_context_data(**kwargs)
        aliases_dict = dict(UserMeterPoint.objects \
            .filter(
                meter_point__meterpointstate__meter_id__in=
                [obj.id for obj in context['object_list']]) \
            .values_list('meter_point__meterpointstate__meter_id', 'alias'))

        for obj in context['object_list']:
            alias = aliases_dict.get(obj.id, '------')
            obj.alias = alias if alias is not None else '------'

        return context


@method_decorator(login_required, name='dispatch')
class RemoveMeterView(DeleteView):
    http_method_names = [u'get', u'post']
    template_name = 'meter_management/remove_meter.html'
    pk_url_kwarg = 'meter_id'
    success_url = 'meter_management:meters_list_view'

    def get_queryset(self):
        return Meter.objects.filter(
            meterpointstate__meter_point__users=self.request.user)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        pk = self.kwargs.get(self.pk_url_kwarg)
        queryset = queryset.filter(meterpointstate__meter_id=pk)
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404

        return obj

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        meter_point = MeterPoint.objects \
            .filter(users=self.request.user,
                    meterpointstate__meter=self.object.id) \
            .first()
        if meter_point is not None:
            UserMeterPoint.objects\
                .filter(meter_point_id=meter_point.id, user_id=request.user.id)\
                .delete()
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super(RemoveMeterView, self).get_context_data(**kwargs)
        context['meter'] = get_object_or_404(
            Meter, meterpointstate__meter_point__users=self.request.user,
            meterpointstate__meter_id=self.object.id
        )
        return context


@method_decorator(login_required, name='dispatch')
class AddMeterView(FormView):
    template_name = 'meter_management/add_meter.html'
    form_class = AddMeterForm
    http_method_names = [u'get', u'post']

    def get_form_kwargs(self):
        kwargs = super(AddMeterView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return redirect('meter_management:meters_list_view')


@method_decorator(login_required, name='dispatch')
class MeterDataView(DetailView):
    template_name = 'meter_management/meter_data.html'
    http_method_names = [u'get', ]
    context_object_name = 'meter'
    model = Meter
    pk_url_kwarg = 'meter_id'

    def get_queryset(self):
        return Meter.objects.filter(
            meterpointstate__meter_point__users=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(MeterDataView, self).get_context_data(**kwargs)
        user_meter_point = UserMeterPoint.objects \
            .filter(
                meter_point__meterpointstate__meter_id=self.object.id,
                user_id=self.request.user.id) \
            .last()
        context['meter'].alias = user_meter_point.alias if \
            user_meter_point.alias else '------'
        return context


@method_decorator(login_required, name='dispatch')
class SetMeterAsMainView(FormView):
    form_class = ChangeMainMeterForm
    http_method_names = [u'get', ]

    redirect_to = 'meter_management:meters_list_view'

    def get_form_kwargs(self):
        return {
            'user': self.request.user,
            'data': self.request.GET,
        }

    def get(self, request, *args, **kwargs):
        if request.GET.get('ref'):
            self.redirect_to = request.GET.get('ref')
        return self.post(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return redirect(self.redirect_to)

    def form_invalid(self, form):
        return redirect(self.redirect_to)


@method_decorator(login_required, name='dispatch')
class ChangeMeterAliasView(FormView):
    http_method_names = [u'get', u'post']
    form_class = ChangeMeterAliasForm
    template_name = 'meter_management/change_meter_alias.html'
    meter = None

    def get(self, request, *args, **kwargs):
        self.meter = get_object_or_404(
            Meter, meterpointstate__meter_point__users=self.request.user,
            id=kwargs.get('meter_id'))
        return super(ChangeMeterAliasView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.meter = get_object_or_404(
            Meter, meterpointstate__meter_point__users=self.request.user,
            id=kwargs.get('meter_id'))
        return super(ChangeMeterAliasView, self).post(request, *args, **kwargs)

    def get_initial(self):
        user_meter_point = UserMeterPoint.objects.filter(
                meter_point__meterpointstate__meter_id=self.meter.id,
                user_id=self.request.user.id).last()
        return {
            'alias': user_meter_point.alias if user_meter_point else ''
        }

    def get_form_kwargs(self):
        kwargs = super(ChangeMeterAliasView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ChangeMeterAliasView, self).get_context_data(**kwargs)
        context['meter'] = self.meter
        return context

    def form_valid(self, form):
        form.save()
        return redirect('meter_management:meters_list_view')


@method_decorator(login_required, name='dispatch')
class AlarmsListView(ListView):
    context_object_name = 'alarms'
    http_method_names = [u'get', ]
    model = Alarm
    page_kwarg = 'strona'
    paginate_by = 10
    template_name = 'meter_management/alarms_list.html'

    def get_queryset(self):
        return Alarm.objects \
            .filter(user_id=self.request.user.id)\
            .select_related('meter')


@method_decorator(login_required, name='dispatch')
class AlarmDetailsView(DetailView):
    template_name = 'meter_management/alarm_data.html'
    http_method_names = [u'get', ]
    context_object_name = 'alarm'
    model = Alarm
    pk_url_kwarg = 'alarm_id'

    def get_queryset(self):
        return Alarm.objects.filter(user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(AlarmDetailsView, self).get_context_data()
        start_date, end_date = \
            self.object.get_period_class().get_period(self.object.period)
        agg_values = MeterData.objects \
            .filter(meter_id=self.object.meter.id,
                    acq_time__range=[start_date, end_date]) \
            .aggregate(maximum=Max('value'), minimum=Min('value'))
        try:
            context['meter_value'] = \
                agg_values.get('maximum', 0) - agg_values.get('minimum', 0)
        except TypeError:
            context['meter_value'] = 0

        return context


@method_decorator(login_required, name='dispatch')
class AddAlarmView(FormView):
    form_class = AddAlarmForm
    http_method_names = [u'get', u'post']
    template_name = 'meter_management/add_alarm.html'

    def get_form_kwargs(self):
        kwargs = super(AddAlarmView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        alarm = form.save()
        return redirect('meter_management:alarm_details_view',
                        alarm_id=alarm.id)


@method_decorator(login_required, name='dispatch')
class EditAlarmView(AddAlarmView):
    alarm_id = None

    def dispatch(self, request, *args, **kwargs):
        self.alarm_id = kwargs.get('alarm_id')
        return super(EditAlarmView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(EditAlarmView, self).get_form_kwargs()
        instance = get_object_or_404(
            Alarm, id=self.alarm_id, user_id=self.request.user.id)
        kwargs.update({'instance': instance})
        return kwargs


class DeleteAlarmView(DeleteView):
    context_object_name = 'alarm'
    model = Alarm
    pk_url_kwarg = 'alarm_id'
    http_method_names = [u'get', u'post']
    template_name = 'meter_management/delete_alarm.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect('meter_management:alarms_list_view')
