#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, MONTHLY, HOURLY, DAILY, YEARLY

from django.db.models import Max, Min

from app.subapps.structure.models import Meter, MeterData


class MeterDataStatistics(object):
    def __init__(self, start_date, end_date, main_meter_point, precision=None):
        self.start_date = start_date + relativedelta(seconds=1)
        self.end_date = end_date + relativedelta(days=1, seconds=-1)
        self.main_meter_point = main_meter_point

        if precision is None:
            self.get_precision()
        else:
            self.get_forced_precision(precision)

    def get_forced_precision(self, precision):
        if precision == 'hour':
            self.before_start_period = self.start_date + relativedelta(hours=-1)
            self.precision = 'hour'
            self.date_string = '%Y-%m-%d %H'
            return

        if precision == 'day':
            self.before_start_period = self.start_date + relativedelta(days=-1)
            self.precision = 'day'
            self.date_string = '%Y-%m-%d'
            return

        if precision == 'month':
            self.before_start_period = self.start_date + relativedelta(months=-1)
            self.precision = 'month'
            self.date_string = '%Y-%m'
            return

        self.before_start_period = self.start_date + relativedelta(years=-1)
        self.precision = 'year'
        self.date_string = '%Y'

    def get_precision(self):
        days_between = (self.end_date - self.start_date).days
        if days_between <= 1:
            self.before_start_period = self.start_date + relativedelta(hours=-1)
            self.precision = 'hour'
            self.date_string = '%Y-%m-%d %H'
            return

        if days_between <= 60:
            self.before_start_period = self.start_date + relativedelta(days=-1)
            self.precision = 'day'
            self.date_string = '%Y-%m-%d'
            return

        if days_between <= 400:
            self.before_start_period = self.start_date + relativedelta(months=-1)
            self.precision = 'month'
            self.date_string = '%Y-%m'
            return

        self.before_start_period = self.start_date + relativedelta(years=-1)
        self.precision = 'year'
        self.date_string = '%Y'

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
        return self.create_data_array(meter_data)

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
        last_value = meter_data.pop(
            self.before_start_period.strftime(self.date_string), 0)
        for date in self.create_loop_range():
            date_value = meter_data.get(date.strftime(self.date_string), 0)
            if date_value:
                meter_data_list.append(date_value - last_value)
                last_value = date_value
            else:
                meter_data_list.append(0)

        return meter_data_list

    def create_loop_range(self):
        if self.precision == 'hour':
            rule = HOURLY
        elif self.precision == 'day':
            rule = DAILY
        elif self.precision == 'month':
            rule = MONTHLY
        else:
            rule = YEARLY

        return (
                dt for dt in
                rrule(rule, dtstart=self.start_date, until=self.end_date)
            )

    def get_other_avg(self):
        aggregated_meter_data = MeterData.objects \
            .filter(acq_time__range=[self.start_date, self.end_date]) \
            .values('meter_id') \
            .annotate(
                maximum=Max('value'),
                minimum=Min('value')
            )[:100]

        sum_values = 0
        for agr_md in aggregated_meter_data:
            sum_values += agr_md.get('maximum') - agr_md.get('minimum')

        return sum_values / len(aggregated_meter_data) \
            if aggregated_meter_data else 0
