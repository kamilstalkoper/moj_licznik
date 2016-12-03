#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django.contrib.auth import login as auth_login, authenticate
from django.shortcuts import get_object_or_404, Http404, redirect
from django.views.generic import FormView

from app.subapps.structure.models import MeterPointState

from ..forms import RegistrationFirstStepForm, RegistrationSecondStepForm


class RegistrationFirstStepView(FormView):
    form_class = RegistrationFirstStepForm
    http_method_names = [u'post', u'get']
    template_name = 'registration/registration_first_step.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('home_view')

        return super(RegistrationFirstStepView, self) \
            .get(request, *args, **kwargs)

    def form_valid(self, form):
        return redirect('registration:registration_second_step_view',
                        meter_point_state_id=form.meter_point_state.id)


class RegistrationSecondStepView(FormView):
    form_class = RegistrationSecondStepForm
    http_method_names = [u'post', u'get']
    template_name = 'registration/registration_second_step.html'

    meter_point_state = None

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('home_view')

        self.meter_point_state = MeterPointState.objects \
            .filter(id=kwargs.get('meter_point_state_id')) \
            .first()

        if self.meter_point_state is None:
            raise Http404

        return super(RegistrationSecondStepView, self) \
            .get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('home_view')

        self.meter_point_state = MeterPointState.objects \
            .filter(id=kwargs.get('meter_point_state_id')) \
            .first()

        if self.meter_point_state is None:
            raise Http404

        return super(RegistrationSecondStepView, self) \
            .post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(RegistrationSecondStepView, self).get_form_kwargs()
        kwargs['meter_point_state'] = self.meter_point_state
        return kwargs

    def form_valid(self, form):
        user = form.save()
        user = authenticate(
            username=user.username, password=form.cleaned_data.get('password1'))
        auth_login(self.request, user)
        return redirect('home_view')
