#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django.db.models import Max

from .models import MeterData


def generate_meter_data_dict(meters_ids, start_date, end_date, data_precision):
    extra_select_dict = {}
    order = []
    values = []
    if data_precision == 'year':
        extra_select_dict['year'] = 'strftime(\'%%Y\', acq_time)'
        order.append('year')
        values.append('year')
    if data_precision == 'month':
        extra_select_dict['month'] = 'strftime(\'%%Y-%%m\', acq_time)'
        order.append('month')
        values.append('month')
    if data_precision == 'day':
        extra_select_dict['day'] = 'strftime(\'%%Y-%%m-%%d\', acq_time)'
        order.append('day')
        values.append('day')
    if data_precision == 'hour':
        extra_select_dict['hour'] = 'strftime(\'%%Y-%%m-%%d %%H\', acq_time)'
        order.append('hour')
        values.append('hour')

    data = MeterData.objects \
        .filter(meter__in=meters_ids, acq_time__gte=start_date,
                acq_time__lte=end_date) \
        .extra(select=extra_select_dict) \
        .values(*values) \
        .order_by(*order) \
        .annotate(Max('value'))

    print data
    return data
