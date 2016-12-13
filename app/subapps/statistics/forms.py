#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from datetime import timedelta

from django import forms

from app.subapps.structure.helpers import generate_meter_data_dict
from app.subapps.structure.models import Meter


class ShowMeterDataForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()

    def __init__(self, *args, **kwargs):
        self.main_meter_point = kwargs.pop('main_meter_point')
        super(ShowMeterDataForm, self).__init__(*args, **kwargs)

    def clean_end_date(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')

        if not start_date:
            # start_date invalid
            return end_date

        if end_date < start_date:
            self.add_error(
                'end_date',
                u'Data końca nie może byc mniejsza od daty początkowej!')
        return end_date

    def get_meter_data(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if self.main_meter_point is None:
            return []

        meters_ids = Meter.objects \
            .filter(meterpointstate__meter_point_id=self.main_meter_point.id) \
            .values_list('id', flat=True)
        day_before_start_date = start_date - timedelta(days=1)
        meter_data = generate_meter_data_dict(
            meters_ids, day_before_start_date, end_date, 'day')

        meter_data = {
            obj['day']: obj['value__max'] for obj in meter_data
        }

        meter_data_list = []
        last_value = meter_data.pop(
            day_before_start_date.strftime('%Y-%m-%d'), 0)
        for i in range((end_date - start_date).days):
            day = start_date + timedelta(days=i)
            day_value = meter_data.get(day.strftime('%Y-%m-%d'), 0)
            if day_value:
                meter_data_list.append(day_value - last_value)
                last_value = day_value
            else:
                meter_data_list.append(0)

        return meter_data_list
