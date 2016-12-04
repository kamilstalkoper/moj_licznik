#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from django import forms

from app.subapps.accounts.forms import RegistrationFirstStepForm
from app.subapps.structure.models import MeterPointState, UserMainMeterPoint


class AddMeterForm(RegistrationFirstStepForm):
    set_as_main = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AddMeterForm, self).__init__(*args, **kwargs)

    def clean(self):
        cd = super(AddMeterForm, self).clean()
        meter_serial_number = cd.get('meter_serial_number')
        ppe_code = cd.get('ppe_code')

        if not (meter_serial_number and ppe_code):
            # meter_serial_number or ppe_code invalid, do not need more
            # validation
            return cd

        if self.meter_point_state.meter_point.users.filter(id=self.user.id)\
                .exists():
            self.add_error('meter_serial_number', u'Masz już ten licznik.')

        return cd

    def save(self):
        self.meter_point_state.meter_point.users.add(self.user)
        if self.cleaned_data.get('set_as_main', False):
            UserMainMeterPoint.objects.filter(user_id=self.user.id).update(
                meter_point=self.meter_point_state.meter_point)


class ChangeMainMeterForm(forms.Form):
    meter_serial_number = forms.CharField(max_length=255)
    meter_point_state = None

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangeMainMeterForm, self).__init__(*args, **kwargs)

    def clean(self):
        cd = super(ChangeMainMeterForm, self).clean()
        meter_serial_number = cd.get('meter_serial_number')

        if not meter_serial_number:
            # meter_serial_number invalid
            return cd

        self.meter_point_state = MeterPointState.objects \
            .filter(meter__serial_number=meter_serial_number) \
            .first()

        if self.meter_point_state is None:
            self.add_error('meter_serial_number', u'Błędny numer licznika.')

        if UserMainMeterPoint.objects.filter(
                meter_point=self.meter_point_state.meter_point,
                user_id=self.user.id).exists():
            self.add_error('meter_serial_number',
                           u'Ten licznik jest już ustawiony jako główny.')

        return cd

    def save(self):
        UserMainMeterPoint.objects.filter(user_id=self.user.id).update(
            meter_point=self.meter_point_state.meter_point)
