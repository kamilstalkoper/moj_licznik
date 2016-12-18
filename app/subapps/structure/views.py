#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from dateutil.relativedelta import relativedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic import TemplateView
from django.utils.timezone import now
from django.utils.decorators import method_decorator

from .enums.standard_enums import TARIFF_DEFINITION_TYPES
from .models import (
    Alarm, UserMeterPoint, MeterPointState, MeterData, TariffDefinition)

from app.subapps.statistics.helpers import MeterDataStatistics
from app.subapps.news.models import Notice, Breakdown


@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    template_name = 'structure/home.html'

    def get_context_data(self, **kwargs):
        context = {}
        context.update({
            'notices': self.get_notices(),
            'breakdowns': self.get_breakdowns(),
        })

        today = now()
        year_ago = today + relativedelta(years=-1)
        user_main_meter_point = UserMeterPoint.objects \
            .filter(user_id=self.request.user.id, is_main_meter_point=True) \
            .first()

        if user_main_meter_point is None:
            context.update({
                'error': u'Proszę ustawić licznik główny.'
            })
            return context

        meter_data_object = MeterDataStatistics(
            year_ago, today, user_main_meter_point.meter_point, precision='day')
        last_year_data = meter_data_object.get_meter_date()

        last_meter_point_state = MeterPointState.objects \
            .filter(meter_point_id=user_main_meter_point.meter_point.id) \
            .select_related('meter', 'tariff') \
            .last()

        last_meter_data = MeterData.objects \
            .filter(meter_id=last_meter_point_state.meter.id) \
            .only('value', 'acq_time').last()

        context.update({
            'last_year': last_year_data,
            'current_limit': last_meter_point_state.current_power_limit,

            'tariff': last_meter_point_state.tariff,
            'tariff_definition_dict': self.get_tariff_definition_dict(
                last_meter_point_state),

            'alarms': self.get_user_alarms(),
        })

        if last_meter_data is not None:
            context.update({
                'last_meter_data_value': last_meter_data.value or 0,
                'last_meter_data_time': last_meter_data.acq_time or None,
            })

        return context

    def get_user_alarms(self):
        return Alarm.objects \
            .filter(user_id=self.request.user.id) \
            .select_related('meter')

    @staticmethod
    def get_tariff_definition_dict(last_meter_point_state):
        tariff_definitions = TariffDefinition.objects \
            .filter(tariff=last_meter_point_state.tariff)
        tariff_definition_dict = {}
        for tariff_definition in tariff_definitions:
            tariff_type_description = TARIFF_DEFINITION_TYPES \
                .get_description_by_number(tariff_definition.tariff_type)
            if tariff_type_description not in tariff_definition_dict.keys():
                tariff_definition_dict[tariff_type_description] = []

            tariff_definition_dict[tariff_type_description].append({
                'start_hour': tariff_definition.start_hour,
                'end_hour': tariff_definition.end_hour,
            })

        return tariff_definition_dict

    def get_notices(self):
        return Notice.objects \
            .filter(Q(users__isnull=True) | Q(users=self.request.user)) \
            .prefetch_related('breakdowns', 'breakdowns__stations') \
            .order_by('-created_at')[:5]

    def get_breakdowns(self):
        return Breakdown.objects \
            .all() \
            .prefetch_related('stations') \
            .order_by('-start_at')
