#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.views.generic import (
    DeleteView, DetailView, ListView, UpdateView, FormView)

from app.subapps.structure.models import Meter, UserMeterPoint

from ..forms import ChangeMeterUsersForm


@method_decorator(staff_member_required(login_url='authentication:auth_login'),
                  name='dispatch')
class MetersListView(ListView):
    context_object_name = 'meters'
    http_method_names = [u'get', ]
    model = Meter
    page_kwarg = 'strona'
    paginate_by = 10
    template_name = 'backend/meters_management/meters_list.html'

    search_phrase = None

    def get(self, request, *args, **kwargs):
        self.search_phrase = escape(request.GET.get('q', ''))
        return super(MetersListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MetersListView, self).get_context_data(**kwargs)
        if not self.search_phrase:
            return context

        context.update({
            'is_searched': True,
            'search_phrase': self.search_phrase,
        })
        return context

    def get_queryset(self):
        qs = Meter.objects.all().order_by('-id')
        if not self.search_phrase:
            return qs

        return qs.filter(
            Q(meterpointstate__meter_point__users__username__icontains=self.search_phrase) |
            Q(serial_number__icontains=self.search_phrase) |
            Q(model_name__icontains=self.search_phrase)
        ).distinct()


@method_decorator(staff_member_required(login_url='authentication:auth_login'),
                  name='dispatch')
class MeterDataView(DetailView):
    template_name = 'backend/meters_management/meter_data.html'
    http_method_names = [u'get', ]
    context_object_name = 'meter'
    model = Meter
    pk_url_kwarg = 'meter_id'
    meter_id = None

    def get(self, request, *args, **kwargs):
        self.meter_id = kwargs.get('meter_id')
        return super(MeterDataView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return Meter.objects.all()

    def get_context_data(self, **kwargs):
        context = super(MeterDataView, self).get_context_data(**kwargs)
        context['meter_users'] = User.objects \
            .filter(
                meterpoint__meterpointstate__meter_id=self.meter_id) \
            .distinct()
        return context


@method_decorator(staff_member_required(login_url='authentication:auth_login'),
                  name='dispatch')
class DeleteMeterView(DeleteView):
    context_object_name = 'meter'
    http_method_names = [u'get', u'post']
    template_name = 'backend/meters_management/delete_meter.html'
    pk_url_kwarg = 'meter_id'
    model = Meter
    queryset = Meter.objects.all()
    success_url = 'backend:meters_list_view'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        UserMeterPoint.objects \
            .filter(meter_point__meterpointstate__meter_id=self.object.id) \
            .delete()
        self.object.delete()
        return redirect(success_url)


@method_decorator(staff_member_required(login_url='authentication:auth_login'),
                  name='dispatch')
class EditMeterDataView(UpdateView):
    context_object_name = 'meter'
    fields = '__all__'
    http_method_names = [u'get', u'post']
    model = Meter
    pk_url_kwarg = 'meter_id'
    template_name = 'backend/meters_management/edit_meter.html'

    def get_success_url(self):
        return '/backend/zarzadzanie_licznikami/dane_licznika/{}'.format(
            self.object.id)


@method_decorator(staff_member_required(login_url='authentication:auth_login'),
                  name='dispatch')
class ChangeMeterUsersView(FormView):
    http_method_names = [u'get', u'post']
    template_name = 'backend/meters_management/edit_meter_users.html'
    form_class = ChangeMeterUsersForm
    meter_id = None

    def dispatch(self, request, *args, **kwargs):
        self.meter_id = kwargs.get('meter_id')
        return super(ChangeMeterUsersView, self) \
            .dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ChangeMeterUsersView, self).get_form_kwargs()
        kwargs['meter_id'] = self.meter_id
        return kwargs

    def get_initial(self):
        return {
            'users': User.objects
                .filter(
                    is_active=True,
                    meterpoint__meterpointstate__meter_id=self.meter_id)
                .distinct()
        }

    def form_valid(self, form):
        form.save()
        return redirect('backend:meters_details_view', meter_id=self.meter_id)
