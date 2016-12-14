#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from datetime import timedelta

from django.views.generic import TemplateView
from django.utils.timezone import now

from .enums.standard_enums import TARIFF_DEFINITION_TYPES
from .models import (
    Alarm, UserMeterPoint, MeterPointState, MeterData, TariffDefinition)

from app.subapps.statistics.helpers import MeterDataStatistics


class HomeView(TemplateView):
    template_name = 'structure/home.html'

    def get_context_data(self, **kwargs):
        today = now()
        first_month_day = today - timedelta(days=today.day)
        user_main_meter_point = UserMeterPoint.objects \
            .filter(user_id=self.request.user.id, is_main_meter_point=True) \
            .first()

        if user_main_meter_point is None:
            last_month_data = []
        else:
            meter_data_object = MeterDataStatistics(
                first_month_day, today, user_main_meter_point.meter_point)
            last_month_data = meter_data_object.get_meter_date()

        last_meter_point_state = MeterPointState.objects \
            .filter(meter_point_id=user_main_meter_point.meter_point.id) \
            .select_related('meter', 'tariff') \
            .last()

        last_meter_data = MeterData.objects \
            .filter(meter_id=last_meter_point_state.meter.id) \
            .only('value', 'acq_time').last()

        return {
            'last_month': last_month_data,
            'current_limit': last_meter_point_state.current_power_limit or 0,
            'last_meter_data_value': last_meter_data.value or 0,
            'last_meter_data_time': last_meter_data.acq_time or None,

            'tariff': last_meter_point_state.tariff,
            'tariff_definition_dict': self.get_tariff_definition_dict(
                last_meter_point_state),

            'alarms': self.get_user_alarms(),
        }

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
