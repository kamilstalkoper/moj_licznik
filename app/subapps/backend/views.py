#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from app.subapps.contact.models import Message, Problem
from app.subapps.news.models import Notice, Breakdown
from app.subapps.structure.models import Meter, MeterPoint


@method_decorator(staff_member_required(login_url='authentication:auth_login'),
                  name='dispatch')
class BackendDashboardView(TemplateView):
    template_name = 'backend/dashboard.html'

    def get_context_data(self, **kwargs):
        return {
            'users_count': User.objects.all().count(),
            'users_staff_count': User.objects.filter(is_staff=True).count(),
            'messges_count': Message.objects.all().count(),
            'problems_count': Problem.objects.all().count(),
            'solved_problems_count': Problem.objects.filter(
                solved=True).count(),
            'notices_count': Notice.objects.all().count(),
            'breakdowns_count': Breakdown.objects.all().count(),
            'notices_breakdowns_count': Notice.objects.filter(
                breakdowns__isnull=False).distinct().count(),
            'meters_count': Meter.objects.all().count(),
            'meter_points_count': MeterPoint.objects.all().count(),
            'meter_points_users_count': MeterPoint.objects.filter(
                users__isnull=False).distinct().count(),
        }
