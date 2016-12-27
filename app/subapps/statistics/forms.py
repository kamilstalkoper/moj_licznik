#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django import forms

from .helpers import MeterDataStatistics

from app.subapps.structure.helpers import get_tariff_data
from app.subapps.structure.models import MeterPointState


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

    def get_meter_data(self, attach_tariff_data=True):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')

        meter_data_object = MeterDataStatistics(
            start_date, end_date, self.main_meter_point)
        meter_data_list = meter_data_object.get_meter_date()

        response_dict = {
            'meter_data': meter_data_list,
            'user_meter_data_sum': sum(meter_data_list),
            'others_avg': meter_data_object.get_other_avg(),
        }
        if attach_tariff_data:
            response_dict.update({
                'tariff_data': get_tariff_data(),
                'current_tariff': MeterPointState.objects
                    .filter(meter_point_id=self.main_meter_point.id)
                    .select_related('tariff')
                    .last().tariff.name
            })

        return response_dict
