#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django import forms

from .helpers import MeterDataStatistics


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

        meter_data_object = MeterDataStatistics(
            start_date, end_date, self.main_meter_point)
        return meter_data_object.get_meter_date()
