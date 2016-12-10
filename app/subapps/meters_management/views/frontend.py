#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, Http404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, DeleteView, FormView, ListView

from app.subapps.structure.models import Meter, MeterPoint, UserMeterPoint

from ..forms import AddMeterForm, ChangeMainMeterForm


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
