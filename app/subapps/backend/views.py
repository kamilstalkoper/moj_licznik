#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


@method_decorator(staff_member_required(login_url='authentication:auth_login'),
                  name='dispatch')
class BackendDashboardView(TemplateView):
    template_name = 'backend/dashboard.html'
