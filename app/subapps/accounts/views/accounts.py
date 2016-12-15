#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView

from app.subapps.structure.models import Meter

from ..forms import EditUserDataForm


@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    http_method_names = [u'get', ]
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        user_meters = Meter.objects \
            .filter(meterpointstate__meter_point__users=self.request.user)
        context['user_meters'] = user_meters
        return context


@method_decorator(login_required, name='dispatch')
class EditUserDataView(FormView):
    http_method_names = [u'get', u'post']
    template_name = 'accounts/edit_profile.html'
    form_class = EditUserDataForm

    def get_initial(self):
        return {
            'email': self.request.user.email,
            'first_name': self.request.user.first_name,
            'last_name': self.request.user.last_name,
        }

    def get_form_kwargs(self):
        kwargs = super(EditUserDataView, self).get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return redirect('accounts:profile_view')
