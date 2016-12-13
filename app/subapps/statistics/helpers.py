#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from datetime import timedelta

from django.db.models import Max

from app.subapps.structure.models import Meter, MeterData


class MeterDataStatistics(object):
    def __init__(self, start_date, end_date, main_meter_point):
        self.start_date = start_date
        self.end_date = end_date
        self.main_meter_point = main_meter_point

        self.precision, period_before, self.date_string = self.get_precision()
        self.before_start_period = start_date - period_before

    def get_precision(self):
        days_between = (self.end_date - self.start_date).days
        if days_between <= 2:
            return 'hour', timedelta(hours=1), '%Y-%m-%d %H'

        if days_between <= 60:
            return 'day', timedelta(days=1), '%Y-%m-%d'

        if days_between <= 400:
            return 'month', timedelta(days=32), '%Y-%m'

        return 'year', timedelta(days=366), '%Y'

    def get_meter_date(self):
        if self.main_meter_point is None:
            return []

        meters_ids = Meter.objects \
            .filter(meterpointstate__meter_point_id=self.main_meter_point.id) \
            .values_list('id', flat=True)
        meter_data = self.generate_meter_data_dict(meters_ids)
        meter_data = {
            obj[self.precision]: obj['value__max'] for obj in meter_data
        }

    def get_extra_select_dict(self):
        extra_select_dict = {}
        if self.precision == 'year':
            extra_select_dict['year'] = 'strftime(\'%%Y\', acq_time)'
        elif self.precision == 'month':
            extra_select_dict['month'] = 'strftime(\'%%Y-%%m\', acq_time)'
        elif self.precision == 'day':
            extra_select_dict['day'] = 'strftime(\'%%Y-%%m-%%d\', acq_time)'
        elif self.precision == 'hour':
            extra_select_dict['hour'] = \
                'strftime(\'%%Y-%%m-%%d %%H\', acq_time)'
        return extra_select_dict

    def generate_meter_data_dict(self, meters_ids):
        extra_select_dict = self.get_extra_select_dict()
        data = MeterData.objects \
            .filter(meter__in=meters_ids,
                    acq_time__gte=self.before_start_period,
                    acq_time__lte=self.end_date) \
            .extra(select=extra_select_dict) \
            .values(self.precision) \
            .order_by(self.precision) \
            .annotate(Max('value'))

        return data

    def create_data_array(self, meter_data):
        meter_data_list = []
        #TODO: add relativedate
        last_value = meter_data.pop(
            self.before_start_period.strftime(self.date_string), 0)
        for i in range((self.end_date - self.start_date).days):
            day = self.start_date + timedelta(days=i)
            day_value = meter_data.get(day.strftime('%Y-%m-%d'), 0)
            if day_value:
                meter_data_list.append(day_value - last_value)
                last_value = day_value
            else:
                meter_data_list.append(0)

        return meter_data_list