#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from datetime import timedelta

from django.views.generic import TemplateView
from django.utils.timezone import now

from .enums.standard_enums import TARIFF_DEFINITION_TYPES
from .models import (
    Alarm, Meter, UserMeterPoint, MeterPointState, MeterData, TariffDefinition)
from .helpers import generate_meter_data_dict


class HomeView(TemplateView):
    template_name = 'structure/home.html'

    def get_context_data(self, **kwargs):
        today = now()
        day_before_first_month_day = today - timedelta(days=today.day)
        user_main_meter_point = UserMeterPoint.objects \
            .filter(user_id=self.request.user.id, is_main_meter_point=True) \
            .first()

        if user_main_meter_point is not None:
            meters = Meter.objects.filter(
                meterpointstate__meter_point_id=
                user_main_meter_point.meter_point.id)
        else:
            meters = Meter.objects.filter(
                meterpointstate__meter_point__users=self.request.user)

        meter_data = generate_meter_data_dict(
            [meter.id for meter in meters], day_before_first_month_day, today,
            'day')
        meter_data = {
            obj['day']: obj['value__max'] for obj in meter_data
        }

        last_month_data = []
        last_value = meter_data.pop(
            day_before_first_month_day.strftime('%Y-%m-%d'), 0)
        first_month_day = day_before_first_month_day + timedelta(days=1)
        for i in range(today.day):
            day = first_month_day + timedelta(days=i)
            day_value = meter_data.get(day.strftime('%Y-%m-%d'), 0)
            if day_value:
                last_month_data.append(day_value - last_value)
                last_value = day_value
            else:
                last_month_data.append(0)

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
